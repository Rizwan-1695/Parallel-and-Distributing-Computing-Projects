import whisper
from multiprocessing import Pool
import os
from moviepy import VideoFileClip

model = None

# model init (parallel optimization)
def init():
    global model
    model = whisper.load_model("base")

# speech-to-text function
def process(file):
    global model
    result = model.transcribe(file, fp16=False)
    return result["text"]

# main logic
def handle_file(file_path):
    ext = file_path.split('.')[-1].lower()

    if ext == "mp4":
        print("🎬 Video detected... Converting to audio")

        video = VideoFileClip(file_path)
        audio_file = "temp_audio.wav"
        video.audio.write_audiofile(audio_file)

        return audio_file

    elif ext == "wav":
        print("🎵 Audio detected...")
        return file_path

    else:
        print("❌ Unsupported file format")
        return None


if __name__ == "__main__":
    file_path = input("Enter file path: ")

    audio_file = handle_file(file_path)

    if audio_file:
        with Pool(2, initializer=init) as p:
            result = p.map(process, [audio_file])

        print("\n📝 Transcription:")
        print(result[0])