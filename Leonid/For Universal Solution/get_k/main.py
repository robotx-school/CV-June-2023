import socket
import pickle
import struct
import cv2
import time
import cam_correct
import numpy as np
import json
import matplotlib.pyplot as plt
import math


h1 = 0
s1 = 160
v1 = 128
h2 = 16
s2 = 250
v2 = 255
h_min = np.array((h1, s1, v1), np.uint8)
h_max = np.array((h2, s2, v2), np.uint8)

clpos = 0
down_pos = [-1, -1]
up_pos = [-1, -1]

try:
    with open('homography.npy', 'rb') as f:
        h = np.load(f)
    with open('height_width.numpy', 'r') as f:
        get_json = json.loads(f.read())
        height = get_json["height"]
        width = get_json["width"]
        
except Exception as err:
    print(err)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
plane_aruco = [0, 1, 2, 3]

def get_image():
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

def cut_img(img):
    global h
    global width
    global height
    global plane_aruco
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray, aruco_dict)
    coords = []
    if res[1] is not None:
        if ([plane_aruco[0]] in res[1] and [plane_aruco[1]] in res[1] and [plane_aruco[2]] in res[1] and [plane_aruco[3]] in res[1]):
            for i in range(4):
                marker = i
                index = np.where(res[1] == marker)[0][0]
                pt0 = res[0][index][0][marker].astype(np.int16)
                coords.append(list(pt0))
                #cv2.circle(img, pt0, 10, (255, 0, 255), thickness = -1)
            height, width, _ = img.shape
            input_pt = np.array(coords)
            output_pt = np.array([[0, 0], [width, 0], [width, height], [0, height]])
            h, _ = cv2.findHomography(input_pt, output_pt)
            with open('homography.npy', 'wb') as f:
                np.save(f, h)
            with open('height_width.numpy', 'w') as f:
                f.write(json.dumps({"height" : height, "width" : width}))
                
    res_img = cv2.warpPerspective(img, h, (width, height))
    #print(res[1])
    left = res_img[0:height, 100:width//2]
    right = res_img[0:height, width//2:width-100]
    return res_img, left , right

def get_rimg():
    frame = get_image()
    frame = cam_correct.undistort(frame)
    try:
        frame, lframe, rframe = cut_img(frame)
    except Exception as err:
            print(err)
    return frame

def get_k(x, y):
    k = -1
    k = round(y/x, 4)
    return k

def on_click(event, x, y, p1, p2):
    global clpos
    global height
    if event == cv2.EVENT_LBUTTONDOWN:
        if clpos == 0:
            cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)
            print(f"down: {[x, y]}")
            clpos += 1
            down_pos[0] = x
            down_pos[1] = y
        elif clpos == 1:
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
            print(f"up: {[x, y]}")
            clpos += 1
            up_pos[0] = x
            up_pos[1] = y
            print(290, x - (width / 2))
            k = [get_k(200, x - (width / 2)), get_k(180, height - y)]
            #600, 400
            print(f"k: {k}")
            

if __name__ == "__main__":
    print("""1. Put the corresponding edge
of the ArUco Marker in
the yellow dot

2. Use the LMB to specify the
lower and upper points of the
ArUco Mmarker (The blue dot should
be in the yellow dot)""")
    while True:
        if clpos == 0:
            frame = get_rimg()
            cv2.circle(frame, (width-100, height//2), 3, (0, 255, 255), -1)
        cv2.imshow("Main", frame)
        cv2.setMouseCallback('Main', on_click)
        key = cv2.waitKey(100) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
