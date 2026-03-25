import requests

cities = {
    "Seattle": (47.6062, -122.3321),
    "Bogota": (4.7110, -74.0721),
    "Singapore": (1.3521, 103.8198),
    "Hilo": (19.7241, -155.0868),
    "Taipei": (25.0330, 121.5654),
    "Reykjavik": (64.1466, -21.9426),
    "Quibdo": (5.6947, -76.6611),
    "Manaus": (-3.1190, -60.0217),
    "Bergen": (60.3929, 5.3220),
    "Juneau": (58.3019, -134.4197),
    "Cherrapunji": (25.2702, 91.7323)
}

for name, (lat, lon) in cities.items():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation_probability"
    try:
        r = requests.get(url, timeout=5).json()
        prob = r.get("hourly", {}).get("precipitation_probability", [0])[0]
        print(f"Checking {name}: {prob}% rain")
        if prob >= 65:
            print(f"\nSUCCESS! Use {name}: {lat}, {lon}")
            break
    except:
        pass
