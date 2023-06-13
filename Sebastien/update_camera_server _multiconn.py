import socket
import cv2
import pickle
import struct
import threading
import time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "192.168.0.222"
port = 9988
socket_address = (host_ip, port)


server_socket.bind(socket_address)


server_socket.listen(5)
print("LISTENING AT:", socket_address)


cap = cv2.VideoCapture(0)


global_frame = None


def update_frame():
    global global_frame
    while cap.isOpened():
        ret, frame = cap.read()
        global_frame = frame

def handle_client(client_socket):
    global global_frame
    if client_socket:
        last_sent_time = time.time()
        while cap.isOpened():
            if time.time() - last_sent_time > 0.3:
                data = pickle.dumps(global_frame)
                message = struct.pack("Q", len(data))+data
                try:
                    client_socket.sendall(message)
                    last_sent_time = time.time()
                except ConnectionResetError:
                    print('Client disconnected')
                    client_socket.close()
                    break

update_thread = threading.Thread(target=update_frame)
update_thread.start()

while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
