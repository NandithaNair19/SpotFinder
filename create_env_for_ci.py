import os
from pathlib import Path

telemetry_env = f"""DRIVERNAME=postgresql+psycopg2
SERVER={os.environ["DB_SERVER"]}
DATABASE={os.environ["DB_NAME"]}
DB_USER={os.environ["DB_USER"]}
DB_PASSWORD={os.environ["DB_PASSWORD"]}
PORT={os.environ["DB_PORT"]}
UUID=test-device
DEVICE_NAME=telemetry-server
TOPIC=spotfinder_gps
"""

web_env = f"""DRIVERNAME=postgresql+psycopg2
SERVER={os.environ["DB_SERVER"]}
DATABASE={os.environ["DB_NAME"]}
DB_USER={os.environ["DB_USER"]}
DB_PASSWORD={os.environ["DB_PASSWORD"]}
PORT={os.environ["DB_PORT"]}
"""

edge_env = """DEVICE_NAME=edge-device
UUID=test-device
TOPIC=spotfinder_gps
DEBUG=0
"""

Path("telemetry-server/.env").write_text(telemetry_env)
Path("web-dashboard/.env").write_text(web_env)
Path("edge-device/.env").write_text(edge_env)

