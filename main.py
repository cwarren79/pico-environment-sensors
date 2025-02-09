import time
import dht
import network
import urequests
import ujson
from pms5003 import PMS5003
from machine import Pin, UART, reset
import config

DHT = dht.DHT22(5)

pms5003 = PMS5003(
    uart=UART(1, tx=Pin(8), rx=Pin(9), baudrate=9600),
    pin_enable=Pin(2),
    pin_reset=Pin(3),
    mode="active",
)


def STA_Setup(ssid, password):
    sta_if = network.WLAN(network.STA_IF)

    # Check if already connected
    if sta_if.isconnected():
        print("Already connected")
        return True

    print("Connecting to", ssid)
    sta_if.active(True)

    # Basic security check
    if sta_if.config("security") == 0:
        print("Warning: Unsecured network")

    try:
        sta_if.connect(ssid, password)

        # Connection timeout loop
        timeout = 15
        while not sta_if.isconnected():
            if timeout <= 0:
                print("Connection timeout")
                sta_if.disconnect()
                # Optional: reset device after multiple failures
                reset()
                return False
            time.sleep(1)
            timeout -= 1

        print("Connected, IP:", sta_if.ifconfig()[0])
        return True

    except OSError as e:
        print("WiFi connection error:", e)
        return False


def get_dht_data():
    try:
        DHT.measure()
        temperature = int(DHT.temperature())
        humidity = int(DHT.humidity())
        print("temperature: %0.2fC  humidity: %0.2f" % (temperature, humidity) + "%")
        result = {"temperature": temperature, "humidity": humidity, "tags": [f"sensor:{config.SENSOR_ID}"]}
    except:
        print("DHT data error")
        result = {}

    return result


def get_pms_data():
    try:
        data = pms5003.read()
        # print(data)

        pm_ug_per_m3 = {
            "1.0um": data.pm_ug_per_m3(1.0),
            "2.5um": data.pm_ug_per_m3(2.5),
            "10um": data.pm_ug_per_m3(10),
        }
        print("pm_ug_per_m3")
        print(pm_ug_per_m3)

        pm_per_1l_air = {
            "0.3um": data.pm_per_1l_air(0.3),
            "0.5um": data.pm_per_1l_air(0.5),
            "1.0um": data.pm_per_1l_air(1.0),
            "2.5um": data.pm_per_1l_air(2.5),
            "5.0um": data.pm_per_1l_air(5.0),
            "10um": data.pm_per_1l_air(10),
        }
        print("pm_per_1l_air")
        print(pm_per_1l_air)
        result = {"pm_ug_per_m3": pm_ug_per_m3, "pm_per_1l_air": pm_per_1l_air, "tags": [f"sensor:{config.SENSOR_ID}"]}
    except:
        print("PMS data error")
        result = {}

    return result


while True:
    try:
        if not STA_Setup(config.WIFI_SSID, config.WIFI_PASSWORD):
            print("WiFi setup failed, retrying in 5 seconds")
            time.sleep(5)
            continue
    except Exception as e:
        print("Error in WiFi setup:", e)
        time.sleep(5)
        continue

    headers = {"content-type": "application/json; charset=utf-8"}
    dht_data = get_dht_data()
    if dht_data == {}:
        time.sleep(1)
        continue
    print(ujson.dumps(dht_data))
    try:
        dht_response = urequests.post(f"https://{config.API_HOST}/dht", headers=headers, data=ujson.dumps(dht_data), timeout=1)
    except:
        print("Request error")
        continue
    print(dht_response.text)

    pms_data = get_pms_data()
    if pms_data == {}:
        time.sleep(1)
        continue
    print(ujson.dumps(pms_data))
    try:
        pms_response = urequests.post(f"https://{config.API_HOST}/pms", headers=headers, data=ujson.dumps(pms_data), timeout=1)
    except:
        print("Request error")
        continue
    print(pms_response.text)
    time.sleep(5)
    dht_response.close()
    pms_response.close()
