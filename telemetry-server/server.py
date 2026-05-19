import json
import time
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def handle_telemetry(client, userdata, message):
    print("\nMessage received from MQTT")

    try:
        payload = json.loads(message.payload.decode())
        print("Raw payload:", payload)
    except Exception as e:
        print("Failed to decode JSON:", e)
        return

    client_name = payload.get("client_name", "unknown_client")
    latitude = payload.get("lat", 0.0)
    longitude = payload.get("lon", 0.0)
    vacant = payload.get("vacant", 0)
    occupied = payload.get("occupied", 0)

    print(f"Telemetry from {client_name}")
    print(f"Lat: {latitude}, Lon: {longitude}")
    print(f"Vacant: {vacant}, Occupied: {occupied}")

    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO parking_lots (client_name, latitude, longitude)
                    VALUES (:client_name, :latitude, :longitude)
                    ON CONFLICT (client_name) DO NOTHING;
                """),
                {
                    "client_name": client_name,
                    "latitude": latitude,
                    "longitude": longitude
                }
            )

            conn.execute(
                text("""
                    INSERT INTO telemetry_data (client_name, vacant, occupied)
                    VALUES (:client_name, :vacant, :occupied)
                    ON CONFLICT (client_name)
                    DO UPDATE SET
                        vacant = EXCLUDED.vacant,
                        occupied = EXCLUDED.occupied,
                        last_updated = CURRENT_TIMESTAMP;
                """),
                {
                    "client_name": client_name,
                    "vacant": vacant,
                    "occupied": occupied
                }
            )

        print(f"Telemetry data stored for {client_name}")

    except Exception as e:
        print("Database operation failed:", e)


def on_connect(client, userdata, flags, rc):
    print("MQTT connect result code:", rc)

    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(client_telemetry_topic)
        print("Subscribed to topic:", client_telemetry_topic)
    else:
        print("MQTT connection failed")


def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker. Code:", rc)


print("Loading .env...")
load_dotenv()

drivername = os.getenv("DRIVERNAME")
server = os.getenv("SERVER")
db = os.getenv("DATABASE")
usr = os.getenv("DB_USER")
pwd = os.getenv("DB_PASSWORD")
port = os.getenv("PORT")
id = os.getenv("UUID")
device_name = os.getenv("DEVICE_NAME")
topic = os.getenv("TOPIC")

print("Checking environment variables...")

required_vars = {
    "DRIVERNAME": drivername,
    "SERVER": server,
    "DATABASE": db,
    "DB_USER": usr,
    "DB_PASSWORD": pwd,
    "PORT": port,
    "UUID": id,
    "DEVICE_NAME": device_name,
    "TOPIC": topic
}

missing = []

for key, value in required_vars.items():
    if not value:
        missing.append(key)

if missing:
    print("Missing environment variables:", missing)
    exit(1)

print("Environment variables loaded")
print("DB server:", server)
print("DB name:", db)
print("DB user:", usr)

conn_url = URL.create(
    drivername=drivername,
    username=usr,
    password=pwd,
    host=server,
    port=int(port),
    database=db
)

print("Creating database engine...")

engine = create_engine(
    conn_url,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10
    },
    pool_pre_ping=True
)

print("Testing Azure PostgreSQL connection...")

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Connected to Azure PostgreSQL")
except Exception as e:
    print("Azure PostgreSQL connection failed:")
    print(e)
    exit(1)

client_name = id + "_" + device_name
client_telemetry_topic = id + "/" + topic

print("MQTT client name:", client_name)
print("MQTT topic:", client_telemetry_topic)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = handle_telemetry
mqtt_client.on_disconnect = on_disconnect

print("Connecting to MQTT broker...")

try:
    mqtt_client.connect("broker.hivemq.com", 1883, 60)
except Exception as e:
    print("MQTT connection failed:")
    print(e)
    exit(1)

mqtt_client.loop_start()

print("Server is running. Waiting for MQTT messages...")

while True:
    try:
        time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        break