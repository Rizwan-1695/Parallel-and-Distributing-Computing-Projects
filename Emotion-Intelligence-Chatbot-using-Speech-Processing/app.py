from flask import Flask, render_template, request

from src.audio_record import record_audio
from src.speech_to_text import speech_to_text
from src.emotion_model import predict_emotion
from src.chatbot import get_response

app = Flask(__name__)

# 🔥 chat history list
chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history

    if request.method == "POST":
        mode = request.form.get("mode")

        user_input = None
        emotion = None
        response = None

        # 🔹 TEXT MODE
        if mode == "text":
            user_input = request.form.get("user_text")

            if user_input:  # empty input check
                emotion = "neutral"

        # 🔹 VOICE MODE
        elif mode == "voice":
            audio = record_audio()
            user_input = speech_to_text(audio)
            emotion = predict_emotion(audio)

        # 🔹 Generate response (only if input exists)
        if user_input:
            response = get_response(user_input, emotion)

            # 🔥 Save to history
            chat_history.append({
                "user": user_input,
                "bot": response,
                "emotion": emotion
            })

    return render_template("index.html", chat_history=chat_history)


if __name__ == "__main__":
    app.run(debug=True)