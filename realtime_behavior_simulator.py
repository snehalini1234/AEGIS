import pandas as pd
import numpy as np
import joblib
import time
import random
import os

# Load trained model and scaler
model = joblib.load("guardian_iso_model.pkl")
scaler = joblib.load("guardian_scaler.pkl")

# Helper: simulate behavioral data
def generate_behavior(normal=True):
    if normal:
        return {
            "precision": np.random.normal(0.9, 0.03),  # typing accuracy
            "speed": np.random.normal(300, 40),        # typing/mouse speed
            "switch_freq": np.random.normal(3, 1)      # app/tab switching
        }
    else:
        return {
            "precision": np.random.normal(0.7, 0.08),
            "speed": np.random.normal(600, 120),
            "switch_freq": np.random.normal(8, 2)
        }

# Helper: clear terminal
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

print("🧠 Starting GuardianFlow Live Behavior Monitor...\n")
time.sleep(1)

# Continuous monitoring loop
for step in range(1, 21):  # simulate 20 sessions
    # Randomly decide if this session is normal or anomalous
    is_normal = random.random() > 0.2  # 80% normal, 20% anomaly
    behavior = generate_behavior(normal=is_normal)
    df = pd.DataFrame([behavior])
    
    # Scale & predict
    X_scaled = scaler.transform(df)
    prediction = model.predict(X_scaled)
    risk_score = (1 - ((model.decision_function(X_scaled) + 0.5))) * 100
    
    # Display results
    clear_console()
    print(f"🧩 Session #{step}")
    print(df)
    print("\n🔍 Risk Score:", round(float(risk_score), 2))
    
    if prediction[0] == -1:
        print("⚠️  ALERT: Anomalous Behavior Detected (Possible Intruder!) 🚨\n")
    else:
        print("✅ Behavior Normal (Trusted User)\n")
    
    # Simulate delay between sessions
    time.sleep(2)

print("\n✅ Simulation completed. GuardianFlow monitor stopped.")
