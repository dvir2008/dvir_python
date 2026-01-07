import socket
import struct
import io
from PIL import Image
import numpy as np # חדש - לטיפול במערכי נתונים
import cv2

HOST_IP = '10.71.46.189' # כפי שציינת
PORT = 8080 
HEADER_SIZE = 8 # גודל הכותרת המציינת את אורך התמונה (Q - 8 בייטים)

def start_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # שימוש ב-SOL_SOCKET ו-SO_REUSEADDR מאפשר שימוש חוזר בפורט מיד
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server_socket.bind((HOST_IP, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST_IP}:{PORT}")

    conn, addr = server_socket.accept()
    print(f"Connection established from: {addr}")
    
    # משתנים לשמירת נתונים
    data = b""
    payload_size = struct.calcsize("Q") # גודל של unsigned long long (8 בייטים)
    
    try:
        while True:
            # 1. קבלת גודל התמונה
            while len(data) < payload_size:
                # קבלת נתונים נוספים (chunk)
                packet = conn.recv(4096) 
                if not packet:
                    # אם אין חבילות נוספות, הלקוח התנתק
                    break 
                data += packet
            
            if not data or len(data) < payload_size:
                break

            # פירוק גודל ההודעה מה-8 בייטים הראשונים
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            
            # 2. קבלת נתוני התמונה
            while len(data) < msg_size:
                data += conn.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # 3. המרה לתמונה והצגה (באמצעות OpenCV)
            
            # המרת נתוני ה-JPEG שנתקבלו למערך NumPy
            np_data = np.frombuffer(frame_data, dtype=np.uint8)
            # פענוח מערך ה-JPEG לתמונת OpenCV
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

            # הצגת התמונה בחלון OpenCV
            cv2.imshow('Remote Desktop Stream', frame)
            
            # אם המשתמש לוחץ על 'q', צא מהלולאה
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except ConnectionResetError:
        print("Client disconnected gracefully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # סגירת כל החלונות והסוקטים
        cv2.destroyAllWindows() 
        conn.close()
        server_socket.close()
        print("Server closed.")

if __name__ == '__main__':
    start_server()