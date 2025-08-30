from pynput.mouse import Controller, Button
import socket

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mouse = Controller()

try:
    client_socket.connect((HOST, PORT))
    print(f"Successfully connected to server at {HOST}:{PORT}")
    
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            print("No data received, closing connection")
            break
        
        print(f"Received data: {data}")  # הדפסה לדיבוג
        
        # פיצול ההודעה
        split_data = data.split(',')
        if len(split_data) < 1:
            print(f"Invalid data format: {data}")
            continue
        
        command = split_data[0]
        
        if command == "move":
            if len(split_data) != 3:
                print(f"Invalid move command format: {data}")
                continue
            try:
                x = int(split_data[1])
                y = int(split_data[2])
                mouse.position = (x, y)
                print(f"Moved mouse to position: ({x},{y})")
            except ValueError as e:
                print(f"Error parsing move coordinates: {e}, data: {data}")
                continue
            
        elif command == "click":
            if len(split_data) != 5:
                print(f"Invalid click command format: {data}")
                continue
            try:
                x = int(split_data[1])
                y = int(split_data[2])
                button = split_data[3]
                pressed_str = split_data[4]
                
                mouse.position = (x, y)
                
                if pressed_str == 'False':
                    mouse.release(Button.left if button == 'Button.left' else Button.right)
                    print(f"Button {button} released")
                else:
                    mouse.press(Button.left if button == 'Button.left' else Button.right)
                    print(f"Button {button} pressed")
            except ValueError as e:
                print(f"Error parsing click coordinates: {e}, data: {data}")
                continue
                
        elif command == "scroll":
            if len(split_data) != 5:
                print(f"Invalid scroll command format: {data}")
                continue
            try:
                x = int(split_data[1])
                y = int(split_data[2])
                dx = int(split_data[3])
                dy = int(split_data[4])
                
                mouse.scroll(dx, dy)
                print(f"Scrolled at position: ({x},{y}) with values dx={dx}, dy={dy}")
            except ValueError as e:
                print(f"Error parsing scroll values: {e}, data: {data}")
                continue
        else:
            print(f"Unknown command: {command}, data: {data}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_socket.close()