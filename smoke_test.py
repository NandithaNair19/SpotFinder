print("Running SpotFinder smoke test...\n")

import os

def check(name, import_function):
    print(f"Checking {name}...")
    try:
        import_function()
        print(f"PASS: {name}\n")
    except Exception as e:
        print(f"FAIL: {name}")
        print(f"Error: {e}\n")
        raise

# Dependency checks
check("python-dotenv import", lambda: __import__("dotenv"))
check("SQLAlchemy import", lambda: __import__("sqlalchemy"))
check("MQTT client import", lambda: __import__("paho.mqtt.client"))
check("Flask import", lambda: __import__("flask"))

# Folder checks
print("Checking project folders...\n")

required_folders = [
    "edge-device",
    "telemetry-server",
    "web-dashboard",
    "model-training"
]

for folder in required_folders:
    print(f"Checking folder: {folder}...")
    if os.path.isdir(folder):
        print(f"PASS: Found folder '{folder}'\n")
    else:
        print(f"FAIL: Missing folder '{folder}'\n")
        raise Exception(f"Missing folder: {folder}")

# File checks
print("Checking important files...\n")

required_files = [
    "requirements.txt",
    ".github/workflows/smoke-test.yml",
    "telemetry-server/.env.example"
]

for file in required_files:
    print(f"Checking file: {file}...")
    if os.path.isfile(file):
        print(f"PASS: Found file '{file}'\n")
    else:
        print(f"FAIL: Missing file '{file}'\n")
        raise Exception(f"Missing file: {file}")

print("All SpotFinder smoke tests passed successfully.")