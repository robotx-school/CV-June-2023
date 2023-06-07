import socket
import pickle
import struct
import cv2
import time

def get_image():
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = '192.168.0.222'
        port = 9988
        client_socket.connect((host_ip, port))

        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            client_socket.close()
            return frame

while True:
    frame = get_image()
    cv2.imshow("img", frame)
    key = cv2.waitKey(100) & 0xFF
    if key == 27:
        break
    if key == 32:
        cv2.imwrite(f"/images/{time.time()}.jpg", frame)
        print(f"Save: /images/{time.time()}.jpg")
cv2.destroyAllWindows()
