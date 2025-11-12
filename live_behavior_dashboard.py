import pandas as pd
import numpy as np
import joblib
import time
import random
import matplotlib.pyplot as plt
from collections import deque
import winsound  # For audio alerts on Windows

# Load the trained model and scaler
model = joblib.load("guardian_iso_model.pkl")
scaler = joblib.load("guardian_scaler.pkl")

# Simulation parameters
num_sessions = 30
risk_scores = deque(maxlen=50)

# Generate simulated behavior data
def generate_behavior(normal=True):
    if normal:
        return {
            "precision": np.random.normal(0.9, 0.03),
            "speed": np.random.normal(300, 40),
            "switch_freq": np.random.normal(3, 1)
        }
    else:
        return {
            "precision": np.random.normal(0.7, 0.08),
            "speed": np.random.normal(600, 120),
            "switch_freq": np.random.normal(8, 2)
        }

# Initialize live plot
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))
line, = ax.plot([], [], lw=2, color='royalblue')
ax.set_ylim(0, 100)
ax.set_xlim(0, 50)
ax.set_xlabel("Session Number")
ax.set_ylabel("Risk Score (%)")
ax.set_title("🧠 GuardianFlow Live Behavioral Risk Dashboard")
ax.grid(True)

print("🚀 Starting GuardianFlow Live Risk Dashboard with Sound Alerts...\n")

for step in range(1, num_sessions + 1):
    # Randomly pick normal or anomalous behavior
    is_normal = random.random() > 0.2
    behavior = generate_behavior(normal=is_normal)
    df = pd.DataFrame([behavior])
    
    # Predict and calculate risk
    X_scaled = scaler.transform(df)
    prediction = model.predict(X_scaled)
    risk_score = (1 - ((model.decision_function(X_scaled) + 0.5))) * 100
    risk_value = round(float(risk_score), 2)
    risk_scores.append(risk_value)
    
    # Update chart
    line.set_data(range(len(risk_scores)), list(risk_scores))
    ax.set_xlim(0, len(risk_scores))
    
    # Change graph color for anomalies and trigger sound
    if prediction[0] == -1:
        line.set_color('crimson')
        status = "⚠️  ANOMALY DETECTED (Possible Intruder)"
        
        # 🔊 Play alert beep sound
        winsound.Beep(1000, 500)  # (frequency, duration in ms)
    else:
        line.set_color('limegreen')
        status = "✅ NORMAL Behavior (Trusted User)"
    
    plt.draw()
    plt.pause(0.5)
    
    print(f"🧩 Session #{step}")
    print(df)
    print(f"🔍 Risk Score: {risk_value} | {status}\n")
    
    time.sleep(1)

plt.ioff()
plt.show()
print("\n✅ Simulation Complete. GuardianFlow Dashboard Stopped.")
