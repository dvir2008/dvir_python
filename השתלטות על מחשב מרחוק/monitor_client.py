import socket
import time
import struct
import io
import mss
from PIL import Image

SERVER_IP = '10.71.46.189' # **וודא שזה תואם לכתובת ה-IP בה השרת מאזין!**
PORT = 8080

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, PORT))
        print(f"Connected to server at {SERVER_IP}:{PORT}")
    except ConnectionRefusedError as e: # שימוש ב-Exception ספציפי יותר (או socket.error)
        print(f"Connection failed: {e}. Check if the server is running and the IP/Port are correct.")
        return

    # מופע של לוכד המסך
    sct = mss.mss()
    # לכידת המסך הראשי (1 = מסך שני, 0 = מסך ראשון, תלוי במערכת)
    monitor = sct.monitors[1]
   
    try:
        while True:
            # 1. לכידת המסך
            sct_img = sct.grab(monitor)
            # המרה לפורמט PIL
            img = Image.frombytes('RGB', (sct_img.width, sct_img.height), sct_img.rgb, 'raw', 'BGR')
           
            # 2. דחיסת התמונה ל-JPEG ושמירה בבייטים בזיכרון
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=80)
            frame_data = img_byte_arr.getvalue()
           
            # 3. שליחת גודל הנתונים (Q = unsigned long long - 8 בייטים)
            client_socket.sendall(struct.pack("Q", len(frame_data)))
           
            # 4. שליחת נתוני התמונה
            client_socket.sendall(frame_data)
           
            # שליחת פריימים בקצב של כ-20 פריימים לשנייה
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Streaming stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred during streaming: {e}")
    finally:
        client_socket.close()
        print("Client socket closed.")

if __name__ == '__main__':
    start_client()