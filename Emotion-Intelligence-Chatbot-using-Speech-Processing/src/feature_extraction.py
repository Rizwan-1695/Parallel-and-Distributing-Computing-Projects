import librosa
import numpy as np

def extract_features(file_path):
    print("📊 Extracting features...")

    # load audio
    y, sr = librosa.load(file_path, duration=5)

    # 🔹 1. MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0)

    # 🔹 2. Pitch (Fundamental Frequency)
    pitch = librosa.yin(y, fmin=50, fmax=300)
    pitch_mean = np.mean(pitch)

    # 🔹 3. Energy (RMS)
    energy = librosa.feature.rms(y=y)
    energy_mean = np.mean(energy)

    # 🔹 4. Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y)
    zcr_mean = np.mean(zcr)

    # 🔹 Combine all features
    features = np.hstack([mfcc_mean, pitch_mean, energy_mean, zcr_mean])

    print("✅ Features extracted!")

    return features


if __name__ == "__main__":
    features = extract_features("audio/input/user_input.wav")
    print("Feature vector shape:", features.shape)
    print("Features:", features)