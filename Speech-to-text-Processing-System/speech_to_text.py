import whisper

# Load model
model = whisper.load_model("base")

def convert_speech_to_text(file_path):
    result = model.transcribe(file_path)
    return result["text"]

if __name__ == "__main__":
    audio_path = r"uploads\download.wav"
    text = convert_speech_to_text(audio_path)
    print("Recognized Text:", text)