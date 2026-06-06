import joblib
import numpy as np
from src.feature_extraction import extract_features

# ✅ load your trained model
model = joblib.load("models/emotion_model.pkl")

# (agar tumne ye labels use kiye thay training me)
labels = ["happy", "sad", "angry", "neutral"]

def predict_emotion(file_path):
    # 🔹 extract features
    features = extract_features(file_path)

    # 🔹 reshape
    features = features.reshape(1, -1)

    # 🔹 prediction
    prediction = model.predict(features)

    # 🔹 agar direct label mil raha hai
    return prediction[0]