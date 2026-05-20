import os
import sys
import importlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "smoke-test-report.txt"

results = []

def check(name, func):
    try:
        func()
        results.append((name, "PASSED", "OK"))
    except Exception as e:
        results.append((name, "FAILED", str(e)))

def check_python():
    assert sys.version_info >= (3, 11), "Python 3.11+ required"

def check_core_dependencies():
    packages = [
        "flask",
        "sqlalchemy",
        "dotenv",
        "paho.mqtt.client",
        "psycopg2",
    ]
    for package in packages:
        importlib.import_module(package)

def check_ml_dependencies():
    packages = [
        "cv2",
        "numpy",
        "ultralytics",
    ]
    for package in packages:
        importlib.import_module(package)

def check_project_folders():
    required = [
        "edge-device",
        "telemetry-server",
        "web-dashboard",
        "requirements.txt",
        "requirements-ml.txt",
    ]
    for item in required:
        assert (ROOT / item).exists(), f"Missing {item}"

def check_env_files():
    required = [
        "telemetry-server/.env",
        "web-dashboard/.env",
        "edge-device/.env",
    ]
    for item in required:
        assert (ROOT / item).exists(), f"Missing {item}"

def check_database_connection():
    from dotenv import load_dotenv
    from sqlalchemy import create_engine, text

    env_path = ROOT / "telemetry-server" / ".env"
    load_dotenv(env_path)

    driver = os.getenv("DRIVERNAME")
    server = os.getenv("SERVER")
    database = os.getenv("DATABASE")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("PORT", "5432")

    missing = []
    for key, value in {
        "DRIVERNAME": driver,
        "SERVER": server,
        "DATABASE": database,
        "DB_USER": user,
        "DB_PASSWORD": password,
        "PORT": port,
    }.items():
        if not value:
            missing.append(key)

    assert not missing, f"Missing DB env variables: {', '.join(missing)}"

    url = f"{driver}://{user}:{password}@{server}:{port}/{database}?sslmode=require"
    engine = create_engine(url, pool_pre_ping=True)

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

check("Python version", check_python)
check("Core dependencies", check_core_dependencies)
check("ML dependencies", check_ml_dependencies)
check("Project folders/files", check_project_folders)
check("Environment files", check_env_files)
check("Database connection", check_database_connection)

passed = sum(1 for _, status, _ in results if status == "PASSED")
failed = sum(1 for _, status, _ in results if status == "FAILED")

with open(REPORT, "w") as f:
    f.write("SpotFinder Smoke Test Report\n")
    f.write("============================\n\n")
    f.write(f"Generated at: {datetime.now()}\n")
    f.write(f"Python: {sys.version}\n\n")
    f.write(f"Summary: {passed} passed, {failed} failed\n\n")

    for name, status, message in results:
        f.write(f"{name}: {status}\n")
        f.write(f"Details: {message}\n\n")

print(REPORT.read_text())

if failed > 0:
    sys.exit(1)