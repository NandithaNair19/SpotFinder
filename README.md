# 🚗 SpotFinder – AI & IoT Based Smart Parking Finder

**SpotFinder** is a real-time, AI-powered parking space detection system that uses **YOLOv8** and **MQTT** to monitor and display live parking availability. Designed for urban parking efficiency, this system was built as part of a hackathon and won the **Runner-Up** position for its practical and innovative use of technology.

---

## 📌 Features

###  Real-Time Detection
- Detects occupied and vacant parking spots using camera feeds.
- Uses YOLOv8 for object detection to ensure high accuracy.

###  IoT Integration
- Uses MQTT protocol to enable lightweight and fast data transmission between edge devices and the server.
- Supports seamless real-time communication.

###  Live Web Dashboard
- Displays parking status with live updates.
- Helps users locate available parking spaces visually and efficiently.

---

## 🛠️ Tech Stack

| Component     | Technology Used         |
|--------------|--------------------------|
| Computer Vision | YOLOv8 (Ultralytics)  |
| Communication | MQTT (Mosquitto Broker) |
| Backend       | Python                  |
| Frontend      | HTML, CSS, JavaScript   |
| Visualization | Real-time Web Dashboard |

---

## 🔄 How It Works

Camera Feed → YOLOv8 Detection → MQTT Publisher → MQTT Broker → MQTT Subscriber → Web 


---

# Architecture

SpotFinder follows a lightweight edge-to-dashboard architecture designed for low latency and modular deployment.

## 1. Edge Layer – Detection & Publishing

The edge device:

* Captures images periodically using a camera module
* Runs YOLOv8 inference locally to detect occupied and vacant parking spaces
* Publishes structured telemetry data as JSON messages through MQTT

## 2. Messaging Layer – MQTT Broker

The MQTT broker:

* Receives telemetry data from edge devices
* Enables lightweight and low-latency communication
* Routes telemetry messages to subscribed services

## 3. Data Layer – PostgreSQL Database

The telemetry server:

* Receives telemetry data from MQTT topics
* Parses parking occupancy and GPS data
* Stores parking metadata and occupancy information in PostgreSQL
* Supports managed PostgreSQL services such as Azure Database for PostgreSQL

## 4. Application Layer – Web Dashboard

The Flask-based dashboard:

* Retrieves parking occupancy data from PostgreSQL
* Displays live parking availability information
* Provides users with navigation support through Google Maps
* Refreshes periodically for near real-time updates

---

# Project Structure

```txt
SpotFinder/
│
├── edge-device/
│   ├── device.py
│   ├── model.py
│   └── model.pt
│
├── telemetry-server/
│   ├── server.py
│   └── .env.example
│
├── web-dashboard/
│   └── app.py
│
├── model-training/
│
├── smoke_test.py
├── requirements.txt
├──requirements-ml.txt
└── README.md
```

---

# Prerequisites

Before running SpotFinder, ensure the following are installed:

* Python 3.10 or later
* pip (Python package manager)
* Git

Optional:

* Raspberry Pi or edge device with a camera module for real hardware deployment
* CounterFit simulator for local edge-device simulation

Verify Python and pip installation:

```bash
python3.11 --version
pip --version
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/NandithaNair19/SpotFinder.git
cd SpotFinder
```

## 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## 3. Install Project Dependencies

```bash
python3.11 -m pip install -r requirements.txt && python3.11 -m pip install -r requirements-ml.txt
```

---

# Dependencies

SpotFinder uses the dependencies listed in `requirements.txt`.

Core libraries and frameworks include:

* Flask
* Flask-SocketIO
* SQLAlchemy
* PostgreSQL (psycopg2)
* paho-mqtt
* OpenCV
* YOLOv8 / Ultralytics
* PyTorch
* CounterFit simulator libraries

All project dependencies can be installed using:

```bash
python3.11 -m pip install -r requirements.txt && python3.11 -m pip install -r requirements-ml.txt
```

---

# Environment Configuration

Create environment files using the provided templates.

## Telemetry Server

```bash
cp telemetry-server/.env.example telemetry-server/.env
```

Update the values in `.env` using the configured PostgreSQL and MQTT credentials.

Required variables:

```env
DRIVERNAME=postgresql+psycopg2
SERVER=<postgres_server>
DATABASE=<database_name>
DB_USER=<database_user>
PASSWORD=<database_password>
PORT=5432

UUID=<device_uuid>
DEVICE_NAME=telemetry-server
TOPIC=<mqtt_topic>
```

---

# Running the Project

## Start the Telemetry Server

```bash
cd telemetry-server
python3.11 server.py
```

## Start the Edge Device Simulator

Open a new terminal:

```bash
cd edge-device
python3.11 device.py
```

## Start the Web Dashboard

Open another terminal:

```bash
cd web-dashboard
python3.11 app.py
```

---

# Smoke Test

SpotFinder includes a lightweight smoke test used to verify that the core project dependencies install correctly and the development environment is configured properly.

Run the smoke test locally using:

```bash
python3.11 smoke_test.py
```

The smoke test validates:

* Python environment setup
* Core dependency imports
* MQTT dependency availability
* SQLAlchemy/database library availability

---

# GitHub Actions CI Workflow

SpotFinder uses GitHub Actions for automated smoke testing on push.

The CI workflow automatically:

* Installs dependencies
* Sets up Python
* Runs the smoke test
* Validates that the project environment is functional

Workflow file location:

```txt
.github/workflows/smoke-test.yml
```

---

# Future Improvements

* Docker-based deployment
* Multi-camera parking support
* Mobile application integration
* Cloud deployment automation

---

## 🏆 Achievement

🥈 Runner-Up at AIOTopia -Gravitas'25
Successfully integrated AI, IoT, and real-time data visualization into a single working prototype within 36 hours.


💙 Made with innovation, teamwork, and a passion for solving real-world problems.
