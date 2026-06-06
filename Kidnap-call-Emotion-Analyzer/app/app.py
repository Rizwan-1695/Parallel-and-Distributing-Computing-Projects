from flask import Flask, render_template, request
import pickle
import numpy as np
import librosa
import tempfile

app = Flask(__name__)

# Load model
model = pickle.load(open("../models/emotion_model.pkl", "rb"))

# Feature extraction
def extract_features(file_path):
    audio, sr = librosa.load(file_path, duration=3)

    mfcc = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=audio, sr=sr).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=audio, sr=sr).T, axis=0)

    return np.hstack([mfcc, chroma, mel])


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    risk = None
    probs = None
    classes = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            # temp file save
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            file.save(temp.name)

            # features
            features = extract_features(temp.name)

            # prediction
            pred = model.predict([features])[0]
            prediction = pred

            # confidence
            probs = model.predict_proba([features])[0]
            classes = model.classes_

            # risk logic
            if pred in ["fear", "angry"]:
                risk = "High Risk (Possible Distress)"
            else:
                risk = "Normal"

    return render_template(
        "index.html",
        prediction=prediction,
        risk=risk,
        probs=probs,
        classes=classes
    )


if __name__ == "__main__":
    app.run(debug=True)