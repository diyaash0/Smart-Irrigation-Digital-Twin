# virtual_sensors.py
import time
import json
import random
import paho.mqtt.client as mqtt

# We use a public broker for the Digital Twin simulation
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "smart_agri/farm123/sensors"

# Configure the MQTT Client
client = mqtt.Client(client_id="Virtual_Sensor_Node_1")

# Virtual environment state
current_moisture = 44.0
current_temp = 25.0

def on_connect(client, userdata, flags, rc):
    print(f"[Virtual Sensor] Connected to MQTT Broker with result code {rc}")
    print(f"[Virtual Sensor] Simulating data and publishing to {MQTT_TOPIC}...")

client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

try:
    while True:
        # Simulate environment changing over time (moisture slowly drops)
        current_moisture -= random.uniform(0.1, 0.5)
        
        # Fluctuate temperature slightly
        current_temp += random.uniform(-0.5, 0.5)
        
        # Prevent impossible values
        current_moisture = max(0.0, min(100.0, current_moisture))
        current_temp = max(-10.0, min(50.0, current_temp))
        
        payload = {
            "sensor_id": "NODE_01",
            "soil_moisture_percent": round(current_moisture, 2),
            "temperature_c": round(current_temp, 2),
            "timestamp": time.time()
        }
        
        # Publish exactly like real IoT hardware
        client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"[Sensor] Published: {payload}")
        
        # Wait 3 seconds before next reading
        time.sleep(3)
        
except KeyboardInterrupt:
    print("Simulation stopped by user.")
    client.loop_stop()
    client.disconnect()