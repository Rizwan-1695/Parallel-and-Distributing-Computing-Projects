import librosa
import numpy as np

def extract_features(file_path):
    # Load audio
    audio, sr = librosa.load(file_path, duration=3)

    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

    # Take mean of MFCC
    mfcc_mean = np.mean(mfcc.T, axis=0)

    return mfcc_mean


# Testing
if __name__ == "__main__":
    file_path = r"audio\input\user_input.wav"
    features = extract_features(file_path)

    print("Features Extracted Successfully")
    print("Features:", features)
    print("Feature Length:", len(features))