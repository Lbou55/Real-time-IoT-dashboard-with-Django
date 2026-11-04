# Real-time IoT Dashboard with Django

A complete Internet of Things (IoT) pipeline that simulates a temperature sensor, processes the data through an MQTT broker, saves it to a local SQLite database and Firebase, and displays it live on a Django WebSocket dashboard.

## 1. System Architecture

This project is divided into two main components:

1. **mqtt_publisher (Data Generation):** A standalone Python script that acts as a virtual IoT sensor. It generates random temperature values and publishes them to a Mosquitto MQTT broker using the `paho-mqtt` library.
2. **gestion_grandeurs (Backend & Frontend):**
   - **Django & Django Channels:** Handles the web server and real-time WebSocket connections using ASGI (`daphne`).
   - **mqttasgi:** Listens to the MQTT broker, intercepts incoming temperature messages, and routes them to the backend.
   - **SQLite:** Stores the historical data (`Grandeurs` and `Mesures`).
   - **Firebase Realtime Database:** Synchronizes the data to the cloud using `pyrebase`.
   - **Redis:** Acts as a Channel Layer to broadcast data from the MQTT consumer to the WebSocket consumers.
   - **Dashboard:** A simple HTML/JS frontend that connects via WebSocket to display live temperature updates.

## 2. Prerequisites

Before running the project, ensure you have the following installed:

1. Python 3.10+
2. Docker Desktop (for running Mosquitto and Redis)
3. Firebase Account (with a Realtime Database created)

## 3. Installation & Setup

### Step 1: Start the Infrastructure (Docker)
Open a terminal and run the Mosquitto broker and Redis server:
```bash
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto mosquitto -c /mosquitto-no-auth.conf
docker run -d --name redis-server -p 6379:6379 redis

Step 2: Setup the Django Backend:

cd gestion_grandeurs
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Step 3: Start the MQTT Consumer (mqttasgi):

python -m mqttasgi.cli --host localhost --port 1883 gestion_grandeur.asgi:application

Step 4: Start the Data Publisher:

cd mqtt_publisher
python -m venv my_env
# On Windows:
my_env\Scripts\activate

pip install -r requirements.txt
python publisher.py

Step 5: View the Dashboard!

Open your browser and navigate to:
http://127.0.0.1:8000/dashboard/
You will see the live temperature values streaming in via WebSockets!

 -Before running this project on your own machine, create your own Firebase project.
 -Generate a private service account key (certificat_firebase.json) and place it in the gestion_grandeurs folder.
 -Update the firebaseConfig dictionary inside gestion_grandeurs/persistance/persistance_engine.py with your own Firebase Web API keys.
 -Ensure your Firebase Realtime Database rules are set to allow read/write for testing: ".read": "true", ".write": "true"
