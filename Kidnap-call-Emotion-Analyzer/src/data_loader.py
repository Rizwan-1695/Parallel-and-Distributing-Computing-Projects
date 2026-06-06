import librosa

def load_audio(file_path):
    audio, sample_rate = librosa.load(file_path, duration=3)
    return audio, sample_rate


# Testing
if __name__ == "__main__":
    file_path = r"audio\input\user_input.wav"
    audio, sr = load_audio(file_path)

    print("Audio Loaded Successfully")
    print("Sample Rate:", sr)
    print("Audio Length:", len(audio))