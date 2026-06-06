import sys
import os
import whisper
from multiprocessing import Pool
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit,
    QVBoxLayout, QFileDialog, QLabel, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from moviepy import VideoFileClip

# ---------- Convert Video to Audio ----------
def video_to_audio(video_file):
    audio_file = video_file + ".wav"
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile(audio_file)
    return audio_file

# ---------- Processing ----------
def process(file):
    model = whisper.load_model("base")
    result = model.transcribe(file, fp16=False)
    return f"{os.path.basename(file)} -> {result['text']}"

# ---------- GUI ----------
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Speech to Text System")
        self.setGeometry(200, 200, 700, 500)

        self.files = []
        self.mode = None

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Arial;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                background-color: #2e2e3e;
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
            }
        """)

        layout = QVBoxLayout()

        # Title
        self.title = QLabel("🎤 Speech to Text Processing System")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Buttons Row
        btn_layout = QHBoxLayout()

        self.btn_audio = QPushButton("🎧 Audio to Text")
        self.btn_audio.clicked.connect(self.select_audio)
        btn_layout.addWidget(self.btn_audio)

        self.btn_video = QPushButton("🎬 Video to Text")
        self.btn_video.clicked.connect(self.select_video)
        btn_layout.addWidget(self.btn_video)

        layout.addLayout(btn_layout)

        # Start Button
        self.btn_process = QPushButton("🚀 Start Processing")
        self.btn_process.clicked.connect(self.run_process)
        layout.addWidget(self.btn_process)

        # Output Box
        self.output = QTextEdit()
        self.output.setPlaceholderText("Output will appear here...")
        layout.addWidget(self.output)

        self.setLayout(layout)

    # ---------- Audio ----------
    def select_audio(self):
        self.mode = "audio"
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Audio", "", "Audio Files (*.wav *.mp3)"
        )
        self.files = files
        self.output.append("✅ Audio files selected\n")

    # ---------- Video ----------
    def select_video(self):
        self.mode = "video"
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Video", "", "Video Files (*.mp4 *.avi)"
        )
        self.files = files
        self.output.append("✅ Video files selected\n")

    # ---------- Process ----------
    def run_process(self):
        if not self.files:
            QMessageBox.warning(self, "Error", "No file selected!")
            return

        self.output.append("⏳ Processing started...\n")

        final_files = []

        if self.mode == "video":
            for f in self.files:
                audio = video_to_audio(f)
                final_files.append(audio)
        else:
            final_files = self.files

        with Pool(4) as p:
            results = p.map(process, final_files)

        self.output.append("\n✅ Results:\n")

        for r in results:
            self.output.append(r)
            self.output.append("--------------------------------------------------")


# ---------- Main ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())