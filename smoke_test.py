print("Running SpotFinder smoke test...")

try:
    import dotenv
    import sqlalchemy
    import paho.mqtt.client as mqtt

    print("Core dependencies imported successfully.")
    print("Smoke test passed.")

except Exception as e:
    print(f"Smoke test failed: {e}")
    raise