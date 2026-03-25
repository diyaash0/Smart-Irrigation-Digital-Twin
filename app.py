# app.py
from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import json
import threading
from ml_model import model
from weather_service import get_hyperlocal_weather

app = Flask(__name__)

# MQTT Setup
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "smart_agri/farm123/sensors"

# Global state to store latest data
latest_data = {
    "moisture": 0.0,
    "temperature": 0.0,
    "predictions": None,
    "weather": None
}

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker!")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        latest_data["moisture"] = payload.get("soil_moisture_percent", 0)
        latest_data["temperature"] = payload.get("temperature_c", 0)
        
        # Every time we get new sensor data, we also fetch weather & run ML
        weather = get_hyperlocal_weather()
        latest_data["weather"] = weather
        
        # Run ML inference
        pred = model.predict_water_need(
            latest_data["moisture"], 
            latest_data["temperature"], 
            weather.get("rain_probability", 0)
        )
        latest_data["predictions"] = pred
        
    except Exception as e:
        print(f"Error processing message: {e}")

# Setup MQTT Client
mqtt_client = mqtt.Client(client_id="Flask_Dashboard_Backend")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def start_mqtt():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

# Start MQTT in a background thread so it doesn't block Flask
threading.Thread(target=start_mqtt, daemon=True).start()

@app.route("/")
def dashboard():
    return render_template("index.html")
    
@app.route("/api/live_data")
def live_data():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
