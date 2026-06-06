import sys
import socket
import threading
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit,
    QVBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox
)

# ---------- CONFIG ----------
HOST = "0.0.0.0"
PORT = 5000

shared_folder = "shared_files"
download_folder = "downloads"

if not os.path.exists(shared_folder):
    os.makedirs(shared_folder)

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# ---------- SERVER ----------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# ---------- GUI CLASS ----------
class PeerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("P2P File Sharing System")
        self.setGeometry(200, 100, 500, 600)

        # Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                background-color: #2e2e3e;
                padding: 5px;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #2e2e3e;
            }
        """)

        layout = QVBoxLayout()

        self.label = QLabel("Peer-to-Peer File Sharing")
        layout.addWidget(self.label)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter Peer IP")
        layout.addWidget(self.ip_input)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Enter Peer Port")
        layout.addWidget(self.port_input)

        self.show_btn = QPushButton("Show Files")
        self.show_btn.clicked.connect(self.show_files)
        layout.addWidget(self.show_btn)

        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        self.download_btn = QPushButton("Download Selected File")
        self.download_btn.clicked.connect(self.download_file)
        layout.addWidget(self.download_btn)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    # ---------- SHOW FILES ----------
    def show_files(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))

            client.send(b"LIST")
            data = client.recv(4096).decode()

            files = data.split(",")

            self.file_list.clear()
            for f in files:
                self.file_list.addItem(f)

            self.log.append("File list loaded successfully")

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # ---------- DOWNLOAD ----------
    def download_file(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())

        selected = self.file_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Error", "Select a file first")
            return

        filename = selected.text()

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))

            client.send(filename.encode())

            data = b""
            while True:
                part = client.recv(4096)
                if not part:
                    break
                data += part

            messages = data.split(b"<<END>>")

            for msg in messages:
                if msg:
                    name, content = msg.split(b"::", 1)
                    fname = name.decode()

                    if content == b"File not found":
                        self.log.append(f"File not found: {fname}")
                    else:
                        path = os.path.join(download_folder, fname)
                        with open(path, "wb") as f:
                            f.write(content)
                        self.log.append(f"Downloaded: {fname}")

            client.close()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


# ---------- SERVER THREAD ----------
def handle_peer():
    while True:
        conn, addr = server.accept()
        request = conn.recv(1024).decode()

        if request == "LIST":
            files = os.listdir(shared_folder)
            conn.send(",".join(files).encode())

        else:
            filenames = request.split(",")
            for filename in filenames:
                filepath = os.path.join(shared_folder, filename)

                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        data = f.read()

                    conn.sendall(filename.encode() + b"::" + data + b"<<END>>")
                else:
                    conn.sendall(filename.encode() + b"::File not found<<END>>")

        conn.close()


# ---------- MAIN ----------
if __name__ == "__main__":
    threading.Thread(target=handle_peer, daemon=True).start()

    app = QApplication(sys.argv)
    window = PeerGUI()
    window.show()
    sys.exit(app.exec_())