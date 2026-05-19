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

load_dotenv()

device_name = os.getenv("DEVICE_NAME", "edge-device")
id = os.getenv("UUID", "test-device")
topic = os.getenv("TOPIC", "spotfinder_gps")

client_name = id + "_" + device_name
client_telemetry_topic = id + "/" + topic

print("Client name:", client_name)
print("MQTT topic:", client_telemetry_topic)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)

print("Connecting to MQTT broker...")
mqtt_client.connect("broker.hivemq.com", 1883, 60)
mqtt_client.loop_start()
print("MQTT connected!")

print("Connecting to CounterFit...")
CounterFitConnection.init("127.0.0.1", 5000)

serial = counterfit_shims_serial.Serial("/dev/ttyAMA0")

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.rotation = 0


def wait_for_gps(max_attempts=20):
    print("Waiting for CounterFit GPS...")

    for attempt in range(max_attempts):
        try:
            line = serial.readline().decode("utf-8", errors="ignore").strip()

            if line and line.startswith("$GPGGA"):
                print("GPS ready")
                return True

        except Exception as e:
            print("GPS check failed:", e)

        print("GPS not ready yet...")
        time.sleep(2)

    print("GPS not ready, using fallback location")
    return False


def wait_for_camera(max_attempts=20):
    print("Waiting for CounterFit camera...")

    for attempt in range(max_attempts):
        try:
            image = io.BytesIO()
            camera.capture(image, "jpeg")
            image.seek(0)

            if len(image.getvalue()) > 1000:
                with open("image.jpg", "wb") as image_file:
                    image_file.write(image.getvalue())

                print("Camera ready")
                return True

        except Exception as e:
            print("Camera check failed:", e)

        print("Camera not ready yet...")
        time.sleep(2)

    print("Camera not ready, using fallback parking counts")
    return False


gps_ready = wait_for_gps()
camera_ready = wait_for_camera()

try:
    while True:
        try:
            # GPS
            line = None

            if gps_ready:
                try:
                    line = serial.readline().decode("utf-8", errors="ignore").strip()

                    if line:
                        print(line)

                except Exception:
                    print("Could not read GPS this round, using fallback location")
                    line = None

            # Camera + YOLO
            if camera_ready:
                try:
                    image = io.BytesIO()
                    camera.capture(image, "jpeg")
                    image.seek(0)

                    with open("image.jpg", "wb") as image_file:
                        image_file.write(image.getvalue())

                    stats = model.predict()

                except Exception as e:
                    print("Camera/model failed this round, using fallback counts")
                    print("Reason:", e)

                    stats = {
                        "vacant": 5,
                        "occupied": 3,
                        "inference_time_ms": 0
                    }
            else:
                stats = {
                    "vacant": 5,
                    "occupied": 3,
                    "inference_time_ms": 0
                }

            # Parse GPS
            if line:
                try:
                    msg = pynmea2.parse(line)
                    stats["lat"] = round(msg.latitude, 9)
                    stats["lon"] = round(msg.longitude, 9)

                except Exception:
                    print("Invalid GPS data, using fallback location")
                    stats["lat"] = 12.9716
                    stats["lon"] = 77.5946
            else:
                stats["lat"] = 12.9716
                stats["lon"] = 77.5946

            stats["client_name"] = client_name

            data = json.dumps(stats)
            print("Sending telemetry:", data)

            mqtt_client.publish(client_telemetry_topic, data)

            time.sleep(10)

        except Exception as e:
            print("Unexpected loop error:", e)
            time.sleep(5)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()