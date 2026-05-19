import os
import time
import io
import json
import pynmea2
import paho.mqtt.client as mqtt
from counterfit_shims_picamera import PiCamera
from counterfit_connection import CounterFitConnection
from dotenv import load_dotenv
import counterfit_shims_serial
import model

print("Starting device.py...")
# Load environment variables
load_dotenv()
device_name = os.getenv('DEVICE_NAME')
id = os.getenv('UUID')
topic = os.getenv('TOPIC')

def print_gps_data(line):
    """Print raw GPS data read from the serial input."""
    print(line.rstrip())


def pad_coordinate(raw_value, direction):
    """
    Pad latitude and longitude strings with leading zeros to match
    the standard NMEA coordinate format.
    """

    if not raw_value:
        return None
    if direction in ['N', 'S']:
        return raw_value.zfill(9)
    elif direction in ['E', 'W']:
        return raw_value.zfill(10)
    return raw_value


def convert_to_decimal(raw_value, direction):
    """
    Convert NMEA GPS coordinates into decimal degrees.
    Latitudes (N/S) have 2 degree digits, longitudes (E/W) have 3 degree digits.
    Returns decimal degree float.
    """
    if not raw_value:
        return None

    raw_value = raw_value.strip()

    # Determine if this is latitude or longitude based on direction
    if direction in ['N', 'S']:
        degree_len = 2
    elif direction in ['E', 'W']:
        degree_len = 3
    else:
        return None  # Invalid direction

    # Split into degrees and minutes
    degrees = float(raw_value[:degree_len])
    minutes = float(raw_value[degree_len:])

    decimal = degrees + (minutes / 60)

    # Apply sign for S/W
    if direction in ['S', 'W']:
        decimal *= -1

    return decimal


# Unique device and topic identifiers
client_name = id + '_' + device_name

# Defining telemetry topic for receiving telemetry
client_telemetry_topic = id + '/' + topic
print("Connecting to MQTT broker...")
# Creating MQTT client and connecting to broker
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)
mqtt_client.connect("broker.hivemq.com", 1883, 60)
mqtt_client.loop_start()
print("MQTT connected!")


# Initialize CounterFit hardware simulator
CounterFitConnection.init('127.0.0.1', 5000)

# Simulated serial GPS module
serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')

# Simulated PiCamera setup
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.rotation = 0


try:
        
    # Infinite loop to continuously capture images, classify and send data
    while True:
        try:
            # Read GPS data line from serial input
            line = serial.readline().decode('utf-8')
            if not line:
                continue

            print_gps_data(line)

            # Capture image from camera and store it in memory
            image = io.BytesIO()
            camera.capture(image, 'jpeg')
            image.seek(0)

            # Store a copy of the latest image
            with open('image.jpg', 'wb') as image_file:
                image_file.write(image.getvalue())

            # Run ML model for parking occupancy detection
            stats = model.predict()

            # Parse GPS NMEA sentence safely
            try:
                msg = pynmea2.parse(line)
                stats["lat"] = round(msg.latitude, 9)
                stats["lon"] = round(msg.longitude, 9)
            except Exception:
                print("Using default demo GPS location")
                stats["lat"] = 12.9716
                stats["lon"] = 77.5946

            stats["client_name"] = client_name

            # Convert data to JSON and publish telemetry data to MQTT topic
            data = json.dumps(stats)
            print("Sending telemetry ", data)
            mqtt_client.publish(client_telemetry_topic, data)

            # Wait for 10 seconds before capturing the next image 
            time.sleep(10)

        except pynmea2.ParseError as e:
            print(f"GPS Parse Error: {e}")

        except Exception as e:
            print(f"Unexpected Error: {e}")


except KeyboardInterrupt:
    print("Exiting...")

finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()