import socket
import os

server_host = '127.0.0.1'
server_port = 1234
download_folder = 'downloads'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_host, server_port))

try:
    # שלב 1: הלקוח מקבל הודעה מהשרת
    server_prompt = s.recv(1024).decode().strip()
    print(server_prompt)

    # שלב 2: הלקוח שולח פקודה
    action = input(">>> ").strip().upper()
    s.sendall(action.encode())

    if action == "UPLOAD":
        # הלקוח מקבל בקשה לשם קובץ
        server_prompt = s.recv(1024).decode().strip()
        print(server_prompt)

        file_to_send = input(">>> ").strip()
        if not os.path.exists(file_to_send):
            print(f"Error: The file '{file_to_send}' was not found.")
        else:
            file_name = os.path.basename(file_to_send)
            s.sendall(file_name.encode())
            
            with open(file_to_send, 'rb') as f:
                chunk = f.read(1024)
                while chunk:
                    s.sendall(chunk)
                    chunk = f.read(1024)
            print(f"File '{file_name}' sent successfully.")

    elif action == "DOWNLOAD":
        # הלקוח מקבל בקשה לשם קובץ
        server_prompt = s.recv(1024).decode().strip()
        print(server_prompt)

        file_name = input(">>> ").strip()
        s.sendall(file_name.encode())

        # הלקוח מקבל את תוכן הקובץ
        file_path = os.path.join(download_folder, file_name)
        with open(file_path, 'wb') as f:
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
        print(f"File '{file_name}' downloaded successfully.")

    else:
        print("Invalid action.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    s.close()