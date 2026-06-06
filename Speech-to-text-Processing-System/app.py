from flask import Flask, render_template, request
import os
from speech_to_text import convert_speech_to_text

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    
    if request.method == "POST":
        file = request.files["audio"]
        
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            text = convert_speech_to_text(filepath)

    return render_template("index.html", text=text)

if __name__ == "__main__":
    app.run(debug=True)