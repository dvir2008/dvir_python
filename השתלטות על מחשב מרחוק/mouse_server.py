import socket
from pynput.mouse import Listener, Button, Controller

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"The server is listening on {HOST} : {PORT}")

client_socket, client_address = server_socket.accept()
print(f"The client {client_address} has connected")

def on_move(x, y):
    message = f"move,{x},{y}"
    client_socket.send(message.encode('utf-8'))

def on_click(x, y, button, pressed):
    message = f"click,{x},{y},{button},{pressed}"
    client_socket.send(message.encode('utf-8'))
    
def on_scroll(x, y, dx, dy):
    message = f"scroll,{x},{y},{dx},{dy}"
    client_socket.send(message.encode('utf-8'))

    with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

client_socket.close()
server_socket.close()           