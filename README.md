# Pico Environment Sensors

A MicroPython project for collecting environmental sensor data using a Raspberry Pi Pico W.

## Setup

1. Clone this repository
2. Copy `config.py.example` to `config.py` and configure it (see Configuration section below)
3. Upload the following files to your Pico W:
   - `main.py` (main program)
   - `pms5003.py` (sensor driver)
   - `config.py` (your configured settings)

## Configuration

The Pico W needs a `config.py` file to store your network and API settings:

1. Copy `config.py.example` to `config.py`
2. Edit `config.py` and update the settings with your values

All configuration options are documented with comments in the example file.

You can upload the required files using any of these methods:

1. Using Thonny (recommended for beginners):
   - Open Thonny IDE
   - Connect your Pico W via USB
   - Click "View" → "Files" to see both your computer and Pico files
   - Copy all required files (`main.py`, `pms5003.py`, and `config.py`) to the Pico
   - Update the configuration values in `config.py`

2. Using VS Code:
   - Install the "Pico-W-Go" extension
   - Connect your Pico W via USB
   - Use the Pico file explorer in the sidebar to upload all required files
   - Create and configure `config.py`

3. Using Cursor or other IDE:
   - Connect your Pico W via USB
   - Mount it as a USB drive
   - Copy all required files to the Pico's root directory
   - Create and configure `config.py`

## Usage

1. Ensure all required files are uploaded to the Pico W
2. Connect the Raspberry Pi Pico W to power
3. The script will start automatically and begin collecting data

For development/debugging:
1. Connect the Pico W to your computer via USB
2. Open a MicroPython REPL (using Thonny or another IDE)
3. Run the script manually by importing and running `main.py`

## Features

- WiFi connectivity using Pico W
- Environmental sensor data collection
- API integration for data transmission

## Requirements

- Raspberry Pi Pico W
- MicroPython firmware installed
- DHT22 temperature and humidity sensor
- PMS5003 particulate matter sensor
- WiFi network access
- HTTP API endpoint to receive sensor data (see API Requirements below)

## API Requirements

The API endpoint specified in `config.py` should:
- Accept POST requests
- Expect JSON data containing sensor readings
- Provide two endpoints:
  1. `/dht` for temperature and humidity data
  2. `/pms` for particulate matter data

The endpoints should support the following data formats:

1. DHT endpoint (`/dht`):
```json
{
    "temperature": int,
    "humidity": int,
    "tags": ["sensor:sensor_id"]
}
```

2. PMS endpoint (`/pms`):
```json
{
    "pm_ug_per_m3": {
        "1.0um": float,
        "2.5um": float,
        "10um": float
    },
    "pm_per_1l_air": {
        "0.3um": float,
        "0.5um": float,
        "1.0um": float,
        "2.5um": float,
        "5.0um": float,
        "10um": float
    },
    "tags": ["sensor:sensor_id"]
}
```
