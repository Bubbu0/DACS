import paho.mqtt.client as mqtt
import json
import time
import random

MQTT_BROKER = "192.168.56.10"
MQTT_PORT = 1883
MQTT_TOPIC = "home/sensors/temperature"
DEVICE_ID = "temp_sensor_01"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client(DEVICE_ID)
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(40.0, 80.0), 2)
        
        payload = {
            "device_id": DEVICE_ID,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": time.time(),
            "battery": random.randint(50, 100)
        }
        
        client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"Published: {payload}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped by user")
    client.disconnect()