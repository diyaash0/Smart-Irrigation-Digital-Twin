import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# 1. Generate Fake Historical Farm Data (1,000 days of history)
print("Generating fake historical agricultural dataset...")
np.random.seed(42)
data_size = 1000

# Features: Soil Moisture (0-100%), Temp (0-50°C), Rain Prob (0-100%)
soil_moisture = np.random.uniform(10, 90, data_size)
temperature = np.random.uniform(15, 45, data_size)
rain_prob = np.random.uniform(0, 100, data_size)

# Label: Was the Pump turned ON (1) or OFF (0) in the past?
pump_on = []
for i in range(data_size):
    if soil_moisture[i] < 45 and rain_prob[i] < 60:
        pump_on.append(1) # Turned on
    elif soil_moisture[i] < 30 and rain_prob[i] >= 60:
        pump_on.append(1) # Critically dry, still turned on despite rain
    else:
        pump_on.append(0) # Kept off

# Create a DataFrame (Excel sheet format)
df = pd.DataFrame({
    'moisture': soil_moisture,
    'temperature': temperature,
    'rain_prob': rain_prob,
    'pump_on': pump_on
})

# 2. Train the Machine Learning Model (Random Forest)
print("Training the Random Forest Neural logic...")
X = df[['moisture', 'temperature', 'rain_prob']]
y = df['pump_on']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# 3. Save the trained "brain" to a .pkl file
with open('irrigation_model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
print("Successfully saved 'irrigation_model.pkl'. Your project now uses real AI!")
