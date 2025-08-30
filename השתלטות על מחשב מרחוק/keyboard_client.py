import socket
from pynput.keyboard import Controller, Key

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

keyboard = Controller()

while True:
    data = client_socket.recv(1024).decode('utf-8')    
    if not data:
        break

    if data.startswith('Key.'):
        key_name = data.split('.')[-1]
        try:
            key = getattr(Key, key_name)
            keyboard.press(key)
            keyboard.release(key)
        except AttributeError:
            pass
    else:
        keyboard.type(data)

client_socket.close()