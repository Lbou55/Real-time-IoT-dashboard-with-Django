import json
import random
import time
from datetime import datetime, timezone
import argparse
import paho.mqtt.client as mqtt

#MQTT Configuration 
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "sensor/temperature"

#Publication interval (seconds)
parser = argparse.ArgumentParser()
parser.add_argument("--interval", type=float, default=1)
args = parser.parse_args()
INTERVAL = args.interval

def generate_mesure():
    return {
        "valeur": round(random.uniform(15.0, 35.0), 2),
        "date_prise": datetime.now(timezone.utc).isoformat()
    }

def main():
    client = mqtt.Client()

    print(f"Connecting to {BROKER_HOST}:{BROKER_PORT}...")
    client.connect(BROKER_HOST, BROKER_PORT, 60)

    client.loop_start()

    try:
        while True:
            mesure = generate_mesure()
            payload = json.dumps(mesure)

            client.publish(TOPIC, payload)
            print(f"Published to: {TOPIC}: {payload}")

            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nStopping publisher...")

    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()