import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)

# Load environment variables
server = os.getenv('SERVER')
db = os.getenv('DATABASE')
usr = os.getenv('DB_USER')
pwd = os.getenv('DB_PASSWORD')
port = os.getenv('PORT')

# Database connection
DB_CONFIG = {
    'host': server,
    'dbname': db,
    'user': usr,
    'password': pwd,
    'port': port,
    'sslmode': 'require'
}


def get_db_connection():
    """Establish and return a PostgreSQL connection."""
    return psycopg2.connect(**DB_CONFIG)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/telemetry", methods=["GET"])
def get_telemetry():
    """Fetch telemetry data from the database and return as JSON."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Build and execute the query
    qry = "SELECT * FROM telemetry_data NATURAL JOIN parking_lots;"
    cur.execute(qry)
    records = cur.fetchall()
    print(records)
    cur.close()
    conn.close()

    return jsonify(records)


if __name__ == "__main__":
    app.run(debug=True, port=8000)