import pandas as pd
import numpy as np
import joblib

# Load the saved model and scaler
model = joblib.load("guardian_iso_model.pkl")
scaler = joblib.load("guardian_scaler.pkl")

# Simulate new user behavior data (you can change values)
new_data = pd.DataFrame([{
    "precision": 0.92,   # typing accuracy
    "speed": 295,        # typing or mouse speed
    "switch_freq": 3.8   # number of tab/app switches
}])

# Scale the new data
X_scaled = scaler.transform(new_data)

# Predict anomaly and calculate risk score
prediction = model.predict(X_scaled)
risk_score = (1 - ((model.decision_function(X_scaled) + 0.5))) * 100

# Display results
print("\n🧠 New User Behavior Analysis:")
print(new_data)
print("\n🔍 Risk Score:", round(float(risk_score), 2))
if prediction[0] == -1:
    print("⚠️ Behavior classified as ANOMALOUS (Possible Intruder!)")
else:
    print("✅ Behavior classified as NORMAL (Trusted User)")
