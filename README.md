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

## 🚀 Prerequisites

Before running the project, make sure you have the following installed:

- ✅ Python 3.8+
- ✅ pip (Python package manager)
- ✅ MQTT Broker (e.g., Mosquitto)

To check if Python and pip are installed:

```bash
python --version
pip --version
```

## 📂 Project Setup & Running the Environment

1️⃣ Clone the Repository
git clone https:https://github.com/NandithaNair19/SpotFinder.git
cd spotfinder

2️⃣ Install Dependencies
pip install ultralytics paho-mqtt opencv-python flask

3️⃣ Start the Detection System
python detect_parking.py

4️⃣ Start the Web Dashboard
python app.py

Once running, visit:
👉 http://localhost:5000/


## 🏆 Achievement

🥈 Runner-Up at AIOTopia -Gravitas'25
Successfully integrated AI, IoT, and real-time data visualization into a single working prototype within 36 hours.


💙 Made with innovation, teamwork, and a passion for solving real-world problems.

