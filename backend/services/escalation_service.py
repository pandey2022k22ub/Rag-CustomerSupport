# services/escalation_services.py
from sklearn.linear_model import LogisticRegression
import numpy as np
import joblib
import os

MODEL_PATH = "models/escalation_model.pkl"

def train_escalation_model(training_data, labels):
    """Train a simple escalation prediction model."""
    model = LogisticRegression()
    model.fit(training_data, labels)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return {"message": "Escalation model trained successfully"}

def predict_escalation(features):
    """Predict escalation risk score."""
    if not os.path.exists(MODEL_PATH):
        return {"error": "Model not trained"}

    model = joblib.load(MODEL_PATH)
    prob = model.predict_proba([features])[0][1]  # probability of escalation
    return {"escalation_risk": round(prob, 2), "needs_escalation": prob > 0.7}
