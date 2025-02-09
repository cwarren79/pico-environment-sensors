import time
from pms5003 import PMS5003
from machine import Pin, UART

print(
    """pms5003_test.py - Continously print all data values.
"""
)


# Configure the PMS5003 for Enviro+
pms5003 = PMS5003(
    uart=UART(1, tx=Pin(8), rx=Pin(9), baudrate=9600),
    pin_enable=Pin(2),
    pin_reset=Pin(3),
    mode="active",
)


while True:
    data = pms5003.read()
    print(data)
    time.sleep(1.0)
