import socket
import os

ip = '127.0.0.1'
port = 1234
upload_folder = 'uploaded_files'

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
s.listen(1)

print(f"Server is listening on {ip}:{port}")

while True:
    connection, address = s.accept()
    print(f"Got a connection from {address}")

    try:
        # שלב 1: השרת שולח ללקוח הודעה לבחור פקודה
        connection.sendall(b"Choose a command: UPLOAD or DOWNLOAD")
        command = connection.recv(1024).decode().strip()
        print(f"Received command: {command}")

        if command == "UPLOAD":
            # שלב 2: השרת מבקש מהלקוח את שם הקובץ
            connection.sendall(b"Enter file name:")
            file_name_bytes = connection.recv(1024)
            file_name = file_name_bytes.decode().strip()
            print(f"Receiving file: {file_name}")

            # שלב 3: השרת מקבל את תוכן הקובץ
            file_path = os.path.join(upload_folder, file_name)
            with open(file_path, 'wb') as f:
                while True:
                    chunk = connection.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"File '{file_name}' saved successfully.")

        elif command == "DOWNLOAD":
            # שלב 2: השרת מבקש מהלקוח את שם הקובץ
            connection.sendall(b"Enter file name:")
            file_name = connection.recv(1024).decode().strip()
            file_path = os.path.join(upload_folder, file_name)
            
            if os.path.exists(file_path):
                # שלב 3: השרת שולח את תוכן הקובץ ללקוח
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        connection.sendall(chunk)
                print(f"File '{file_name}' sent to client.")
            else:
                connection.sendall(b"ERROR: File not found.")
                print(f"Error: File '{file_name}' not found.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()

s.close()