import pickle
import warnings
warnings.filterwarnings("ignore") # Ignore sklearn warnings

class IrrigationModel:
    def __init__(self):
        try:
            # Load the actual trained Machine Learning model
            with open('irrigation_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            self.model_loaded = True
            print("[ML Engine] Successfully loaded trained AI Model (irrigation_model.pkl)")
        except FileNotFoundError:
            print("[ML Engine] Warning: irrigation_model.pkl not found. Please run train_ml.py first!")
            self.model_loaded = False

    def predict_water_need(self, soil_moisture, temperature, rain_prob):
        """
        Uses the Random Forest model to predict if we need water.
        """
        if not self.model_loaded:
            return {
                "needs_water": False,
                "duration_minutes": 0,
                "reason": "Model not trained. Run train_ml.py",
                "confidence": 0.0
            }

        # The ML Model takes a 2D array of the real-time sensor data
        prediction = self.model.predict([[soil_moisture, temperature, rain_prob]])[0]
        
        # Get the actual AI confidence percentage
        probabilities = self.model.predict_proba([[soil_moisture, temperature, rain_prob]])[0]
        confidence = round(max(probabilities), 2)

        if prediction == 1:
            # The AI determined the pump needs to turn ON
            # We calculate optimal water duration based on temperature evaporation
            evaporation_factor = temperature / 40.0
            duration = int(30 * (1 + evaporation_factor))
            
            return {
                "needs_water": True,
                "duration_minutes": duration,
                "reason": "AI Random Forest predicted critical soil stress based on historical farm data.",
                "confidence": confidence
            }
        else:
            return {
                "needs_water": False,
                "duration_minutes": 0,
                "reason": "AI Random Forest predicted optimal conditions. Pump remains on standby.",
                "confidence": confidence
            }

model = IrrigationModel()
