import socket
import threading
import os

HOST = "0.0.0.0"
PORT = int(input("Enter your port: "))

shared_folder = "shared_files"
download_folder = "downloads"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Peer running on port", PORT)

def handle_peer():
    while True:
        conn, addr = server.accept()
        request = conn.recv(1024).decode()
        # If peer asks for file list
        if request == "LIST":
            files = os.listdir(shared_folder)
            file_list = ",".join(files)
            conn.send(file_list.encode())
        # If peer requests files
        else:
            filenames = request.split(",")
            for filename in filenames:
                filepath = os.path.join(shared_folder, filename)
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        data = f.read()
                    conn.sendall(filename.encode() + b"::" + data + b"<<END>>")
                    print("Sent file:", filename)
                else:
                    conn.sendall(filename.encode() + b"::File not found<<END>>")
        conn.close()
def request_peer():
    while True:
        print("\n1. Show files")
        print("2. Download file")
        choice = input("Enter choice: ")
        ip = input("Enter peer IP: ")
        port = int(input("Enter peer port: "))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        # show files
        if choice == "1":
            client.send(b"LIST")
            data = client.recv(4096).decode()
            files = data.split(",")
            print("\nAvailable files:")
            for f in files:
                print(f)
        # download files
        elif choice == "2":
            filenames = input("Enter file name (comma separated for multiple): ")
            client.send(filenames.encode())
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
                    filename = name.decode()
                    if content == b"File not found":
                        print("File not available:", filename)
                    else:
                        path = os.path.join(download_folder, filename)
                        with open(path, "wb") as f:
                            f.write(content)
                        print("File downloaded:", filename)
        client.close()

threading.Thread(target=handle_peer, daemon=True).start()

request_peer()