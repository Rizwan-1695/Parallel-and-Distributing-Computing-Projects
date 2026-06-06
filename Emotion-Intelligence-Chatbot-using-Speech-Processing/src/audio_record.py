import sounddevice as sd
from scipy.io.wavfile import write
import os

def record_audio(filename="audio/input/user_input.wav", duration=5, fs=44100):
    print("🎤 Recording started... Speak now!")

    # record audio
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    print("✅ Recording finished!")

    # folder create if not exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # save file
    write(filename, fs, recording)

    print(f"💾 Audio saved at: {filename}")

    return filename


# test run
if __name__ == "__main__":
    record_audio()