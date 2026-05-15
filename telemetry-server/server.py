import json
import time
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine,text
from sqlalchemy.engine import URL


def handle_telemetry(client, userdata, message):
    """
    Function to handle incoming telemetry messages from MQTT broker.

    Decodes the JSON payload from the received message and prints
    the telemetry data sent by IoT clients.
    """

    payload = json.loads(message.payload.decode())
    print("Message received:")

    client_name = payload.get("client_name", "unknown_client")
    latitude = payload.get("lat", 0.0)
    longitude = payload.get("lon", 0.0)
    vacant = payload.get("vacant", 0)
    occupied = payload.get("occupied", 0)
    print(f"Telemetry from {client_name}\nLat: {latitude}, Lon: {longitude}, Vacant: {vacant}, Occupied: {occupied}")
    try:
        with connection.begin():  # automatically commits or rolls back
            # Ensure parking lot exists
            connection.execute(
                text(
                """
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

            # Insert or update telemetry data
            connection.execute(
                text(
                """
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

        print(f"Telemetry data stored for {client_name}\n")

    except Exception as e:
        print(f"Database operation failed: {e}")


# Loading environment variables
load_dotenv()

drivername = os.getenv('DRIVERNAME')
server = os.getenv('SERVER')
db = os.getenv('DATABASE')
usr = os.getenv('DB_USER')
pwd = os.getenv('PASSWORD')
port = os.getenv('PORT')
id = os.getenv('UUID')
device_name = os.getenv('DEVICE_NAME')
topic = os.getenv('TOPIC')

# Creating database connection
conn_url = URL.create(
    drivername=drivername,
    username=usr,
    password=pwd,
    host=server,
    port=port,
    database=db
)

# Establishing connection
engine = create_engine(
    conn_url,
    connect_args={"sslmode": "require"}
)
connection = engine.connect()


# Defining unique device ID and client name
client_name = id + '_' + device_name

# Defining telemetry topic for receiving telemetry
client_telemetry_topic = id + '/' + topic

# Creating an MQTT client and connecting to the broker
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_name)
mqtt_client.connect("test.mosquitto.org", 1883)

# Starting the MQTT client loop in background
mqtt_client.loop_start()

# Subscribing to telemetry topic and assigning function to handle incoming MQTT messages
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    try:
        time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
        break