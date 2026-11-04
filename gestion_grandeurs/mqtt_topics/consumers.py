import json
from mqttasgi.consumers import MqttConsumer
from persistance.persistance_engine import persist_mesure, persist_to_firebase

class MyMqttConsumer(MqttConsumer):

    async def connect(self):
        print("DEBUG 1: MQTT connect()")
        await self.subscribe('sensor/temperature', 2)
        print("DEBUG 2: subscribed to sensor/temperature")

        self.room_group_name = 'sensor_temperature'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("DEBUG 3: joined Redis group")

    async def receive(self, mqtt_message):
        print("DEBUG 4: MQTT MESSAGE RECEIVED")
        payload = mqtt_message['payload'].decode("utf-8")
        print(f"Payload: {payload}")

        # Save to Database first, then Firebase
        try:
            await persist_mesure(payload)
            await persist_to_firebase(payload)
            print("DEBUG 4b: measurement saved in database and firebase")
        except Exception as e:
            print(f"ERROR while persisting: {e!r}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "sensor.temperature",
                "message": {
                    "payload": payload
                }
            }
        )
        print("DEBUG 5: message sent to group")

    async def sensor_temperature(self, event):
        print("DEBUG 6: sensor_temperature() called")
        print("EVENT:", event)

    async def disconnect(self):
        print("DEBUG 7: MQTT disconnected")
        await self.unsubscribe('sensor/temperature')