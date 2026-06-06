import whisper

def speech_to_text(audio_path="audio/input/user_input.wav"):
    print("⏳ Loading Whisper model...")

    # load model (small is fast, medium better, base balanced)
    model = whisper.load_model("base")

    print("🎧 Converting speech to text...")

    result = model.transcribe(audio_path)

    text = result["text"]

    print("📝 Recognized Text:", text)

    return text


# test run
if __name__ == "__main__":
    speech_to_text()