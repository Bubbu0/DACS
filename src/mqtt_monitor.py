import paho.mqtt.client as mqtt
import json
import ssl
import time
from datetime import datetime
import logging

# Cấu hình logging
logging.basicConfig(
    filename='/var/log/mqtt_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MQTT_BROKER = "192.168.56.10"
MQTT_PORT = 8883
MQTT_USER = "admin"
MQTT_PASSWORD = "admin_password"
CA_CERT = "/etc/mosquitto/certs/ca.crt"

# Thresholds
TEMP_MAX = 50.0
TEMP_MIN = 10.0
MESSAGE_RATE_MAX = 2  # messages per second

message_count = {}
last_check = time.time()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Monitor connected successfully")
        client.subscribe("#")
    else:
        logging.error(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    global message_count, last_check
    
    try:
        payload = json.loads(msg.payload.decode())
        
        # Check temperature anomaly
        if 'temperature' in payload:
            temp = payload['temperature']
            if temp > TEMP_MAX or temp < TEMP_MIN:
                logging.warning(f"Temperature anomaly detected: {temp}°C on topic {msg.topic}")
        
        # Track message rate
        topic = msg.topic
        current_time = time.time()
        
        if topic not in message_count:
            message_count[topic] = []
        
        message_count[topic].append(current_time)
        
        # Clean old entries
        message_count[topic] = [t for t in message_count[topic] if current_time - t < 1]
        
        # Check rate
        if len(message_count[topic]) > MESSAGE_RATE_MAX:
            logging.warning(f"High message rate detected on topic {topic}: {len(message_count[topic])} msg/s")
            
    except Exception as e:
        logging.error(f"Error processing message: {e}")

client = mqtt.Client("MonitorClient")
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(ca_certs=CA_CERT, cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

logging.info("Starting MQTT monitor...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()