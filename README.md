# Django IoT Dashboard
Real-time IoT monitoring platform built with Django, Django Channels, MQTT and WebSockets.

## 🎯 Overview
This project demonstrates a complete IoT data pipeline:


It receives measurements published to MQTT topics, broadcasts them in real time
to a web dashboard via WebSockets, and persists them to a database
(SQLite + Firebase Realtime Database).

## 🏗️ Architecture

- **Django** — Web framework and ORM
- **Django Channels** — Async/WebSocket support (ASGI)
- **mqttasgi** — Bridge between MQTT broker and Django consumers
- **Mosquitto** — MQTT broker (publish/subscribe)
- **Redis** — Channel layer (message queue between MQTT and WebSocket)
- **Firebase** — Realtime cloud database (via `pyrebase`)
- **SQLite** — Local persistence
- **Docker** — Runs Mosquitto and Redis containers

## 📦 Django Apps

| App | Role |
|-----|------|
| `website` | Public website |
| `grandeurs` | Data model (measured quantities + measurements) |
| `mqtt_topics` | MQTT consumer (subscribes to broker) |
| `dashboard` | WebSocket consumer + real-time UI |
| `persistence` | Firebase persistence engine |

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- Docker Desktop (for Mosquitto + Redis)

### 2. Start infrastructure

```bash
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto
docker run -d --name redis-server -p 6379:6379 redis
