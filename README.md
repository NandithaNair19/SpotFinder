# SpotFinder

**SpotFinder** is a parking space detection system that leverages computer vision and IoT communication to detect and display parking space availability. The system provides near real-time parking availability updates using **YOLOv8** for parking space detection and **MQTT** for lightweight, low-latency data transmission from low-power and resource constrained edge devices.

🥈 **SpotFinder** was awarded the Runner-Up position at the AIoTopia hackathon 2025.

## Features

###  Real-Time Detection
* Detects occupied and vacant parking spots using live camera feeds.
* Utilizes YOLOv8 for accurate and efficient object detection.

###  IoT-Based Communication
* Uses MQTT protocol to enable lightweight and low latency data transmission between edge devices and the server.
* Enables real-time communication between edge devices and the server.

###  Live Web Dashboard
* Displays current parking availability with live updates
* Provides GPS coordinates of available parking spots for easy navigation.

## Architecture

SpotFinder follows a lightweight edge-to-dashboard architecture designed for low latency and modular deployment. The system separates detection, messaging, and visualization into independent components for scalability and maintainability.

### 1. Edge Layer - Detection & Publishing

* Captures photos every 10 seconds using a camera.
* Runs inference on edge using the YOLOv8 model to detect parking space occupancy.
* Publishes structured telemetry data as JSON messages to an MQTT topic.

### 2. Messaging Layer - MQTT Broker

* Receives telemetry data from edge devices by subscribing to the MQTT topic.
* Parses JSON payloads to extract parking space status and GPS coordinates.
* Performs upsert operations on the database to persist the latest parking space information.

### 3. Data Layer - Relational Database

* * Uses PostgreSQL as the relational database backend. The current setup supports managed PostgreSQL services such as Azure Database for PostgreSQL.
* Stores parking lot metadata and live parking occupancy status.

### 4. Application Layer - Web Dashboard  

* Flask-based web server that retrieves occupancy data from the AWS RDS database.
* Provides users with an option to navigate to a parking lot using Google Maps.
* Refreshes periodically to provide near real-time monitoring of parking space availability.

## Getting Started

### Prerequisites

Before running the project, make sure you have the following installed:

✅ Python 3.10+\
✅ pip (Python package manager)\
✅ An MQTT Broker (e.g., Mosquitto or AWS IoT Core)\
✅ Edge processing unit with a camera module (e.g., Raspberry Pi)\
✅ Verify that your database server is running.

To check if Python and pip are installed:

```bash
python --version
pip --version
```

### Installation

1. Clone the Repository
```
git clone https://github.com/amanamitabh/SpotFinder.git
cd spotfinder
```

2. Install Dependencies
```
pip install -r requirements.txt
```

3. Create a .env file in the edge-device directory and add the following environment variables:
```
DEVICE_NAME=<your_device_name>
UUID=<your_device_uuid>
TOPIC=<your_mqtt_topic>
DEBUG=<1 for debug mode or 0 for production mode>
```

4. Create a .env file in the telemetry-server directory and add the following environment variables:
```
PASSWORD=<your_database_password>
DATABASE=<your_database_name>
USER=<your_database_user>
SERVER=<your_database_server>
PORT=<your_database_port>
DRIVERNAME=<your_database_driver_name>
UUID=<your_server_uuid>
DEVICE_NAME=<your_server_device_name>
TOPIC=<your_mqtt_topic>
```

5. Create a .env file in the web-dashboard directory and add the following environment variables:
```
PASSWORD=<your_database_password>
DATABASE=<your_database_name>
USER=<your_database_user>
SERVER=<your_database_server>
PORT=<your_database_port>
```
6.  Copy the edge-device/ directory to your edge processing unit (e.g., Raspberry Pi) and run the edge device script:
```
python edge_device.py
```

7. Copy the telemetry-server/ directory to your telemetry server and run the script:
```
python server.py
```

8. Copy the web-dashboard/ directory to the web server and run the web dashboard script:
```
python app.py
```