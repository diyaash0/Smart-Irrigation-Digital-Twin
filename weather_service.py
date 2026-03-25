# weather_service.py
import requests

# Global variable to remember the last successful weather
last_weather = {
    "temperature_c": 25.0,
    "rain_probability": 0.0,
    "status": "fallback"
}

def get_hyperlocal_weather():
    global last_weather
    
    # Latitude and longitude (Bergen, Norway .....)
    lat, lon = 36.1716, -115.1390
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation_probability&timezone=auto"
    
    try:
        response = requests.get(url, timeout=2)
        data = response.json()
        
        prob_precip = data.get("hourly", {}).get("precipitation_probability", [0])[0]
        cur_temp = data.get("current_weather", {}).get("temperature", 25.0)
        
        # Save the successful data to our global cache
        last_weather = {
            "temperature_c": cur_temp,
            "rain_probability": prob_precip,
            "status": "success"
        }
        return last_weather
    except Exception as e:
        # If the API times out, gracefully use the last known weather instead of crashing to 0%
        return last_weather
