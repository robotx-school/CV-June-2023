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
from insert_Image import *
from lib_ import *
from get_robot_coords import *

h1 = 0
s1 = 160
v1 = 128
h2 = 16
s2 = 250
v2 = 255
h_min = np.array((h1, s1, v1), np.uint8)
h_max = np.array((h2, s2, v2), np.uint8)

#aruco_img = create_aruco_marker(17)

gk = [-1, -1]
#plt.ion()
#figure, ax = plt.subplots(figsize=(10, 8))
#line1, = ax.plot([0, 0], [1, 0])
#plt.title("Plot", fontsize=20)
#plt.xlabel("X-axis")
#plt.ylabel("Y-axis")





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

def get_aruco_pos(img, k = 1.6, z = 1.3):
    global h
    global width
    global height
    global plane_aruco
    rpt0 = []
    rimg = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray, aruco_dict)
    coords = {}
    if res[1] is not None:
        for i in range(4, 251):
        #for i in range(17):
            if ([i] in res[1]):
                print(i, "detected")
                pt1 = [-1, -1]
                pt2 = [-1, -1]
                marker = i
                index = np.where(res[1] == marker)[0][0]
                pt0 = res[0][index][0].astype(np.int16)
                for pos in pt0:
                    cv2.circle(rimg, pos, 10, (255, 0, 255), thickness =-1)
                rpt0.append(pt0)
                pt1 = [(pt0[0][0] + pt0[1][0] + pt0[2][0] + pt0[3][0])//4,
                                 (pt0[0][1] + pt0[1][1] + pt0[2][1] + pt0[3][1])//4]
                cv2.circle(rimg, pt1, 10, (0, 255, 0), thickness =-1)
                pt2 = [round(pt1[0]/z), round(pt1[1]/k)]
                coords[i] = [pt1, pt2]
                #print(f"{i}: {pt0}; {pt1}")
                #cv2.circle(img, pt0, 10, (255, 0, 255), thickness = -1)
            #height, width, _ = img.shape
            #input_pt = np.array(coords)
            #output_pt = np.array([[0, 0], [width, 0], [width, height], [0, height]])
            #h, _ = cv2.findHomography(input_pt, output_pt)
            #with open('homography.npy', 'wb') as f:
            #    np.save(f, h)
            #with open('height_width.numpy', 'w') as f:
            #    f.write(json.dumps({"height" : height, "width" : width}))
                
    #res_img = cv2.warpPerspective(img, h, (width, height))
    #print(res[1])
    return [coords, rimg, rpt0]

def get_shape_pos(frame):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img_bin = cv2.inRange(frame_hsv, h_min, h_max)
    #print(np.sum(img_bin, axis=1))
    #print(len(np.sum(img_bin, axis=1)))
    data = [-1, -1, -1, -1]
    shape_detected = 0
    """for i in range(len(np.sum(img_bin, axis=1))):
        if np.sum(img_bin, axis=1)[i] >= 20000 and np.sum(img_bin, axis=1)[i] <= 26000 and not bde:
            data[2] = i
            bde = True
        elif np.sum(img_bin, axis=1)[i] >= 20000 and not ide:
            data[0] = i
            ide = True
        elif np.sum(img_bin, axis=1)[i] <= 20000 and ide:
            data[1] = i
            break
    """
    ide = False
    bde = False
    for i in range(len(np.sum(img_bin, axis=1))):
        if np.sum(img_bin, axis=1)[i] >= 20000 and np.sum(img_bin, axis=1)[i] <= 26000 and not bde:
            data[2] = i
            bde = True
        elif np.sum(img_bin, axis=1)[i] >= 20000 and not ide:
            data[0] = i
            ide = True
    
    ide = False
    bde = False
    for i in range(len(np.sum(img_bin, axis=1))-1, -1, -1):
        if np.sum(img_bin, axis=1)[i] >= 20000 and np.sum(img_bin, axis=1)[i] <= 26000 and not bde:
            data[3] = i
            bde = True
        elif np.sum(img_bin, axis=1)[i] >= 20000 and not ide:
            data[1] = i
            ide = True
    print(data)

    rframe = frame.copy()
    rframe = cv2.line(rframe, (0, data[0]), (800, data[0]), (255, 0, 0), 9)
    rframe = cv2.line(rframe, (0, data[1]), (800, data[1]), (255, 0, 0), 9)
    rframe = cv2.line(rframe, (0, data[2]), (800, data[2]), (0, 0, 255), 3)
    rframe = cv2.line(rframe, (0, data[3]), (800, data[3]), (0, 0, 255), 3)

    return [data, rframe, img_bin]

def get_angle(img):
    aruco_coords = get_aruco_pos(img)[2]
    print("get_aruco", aruco_coords)
    if aruco_coords != []:
        rytp = []
        for aruco_coords_temp in aruco_coords:
            pt0_ = aruco_coords_temp[0]
            pt1_ = aruco_coords_temp[1]
            tmp_angle = 0
            kat_0 = pt1_[0] - pt0_[0]
            kat_1 = pt1_[1] - pt0_[1]
            tg = kat_1 / kat_0
            tmp_angle = math.atan(tg)
            tmp_angle = math.degrees(tmp_angle)
            tmp_angle = math.fabs(tmp_angle)
            tmp_angle = int(tmp_angle)
            rytp.append(tmp_angle)
        return rytp
    else:
        return None

"""
while True:
    frame = get_image()
    frame = cam_correct.undistort(frame)
    try:
        frame, lframe, rframe = cut_img(frame)
        cv2.imshow("lMain", lframe)
        cv2.imshow("rMain", rframe)
        aruco = get_aruco_pos(rframe)
        #print(f"aruco: {aruco}")
        #aruco[0][17][1][0] += 290
    except Exception as err:
        print(err)


    #line1.set_xdata(range(len(np.sum(img_bin, axis=1))))
    #line1.set_ydata(np.sum(img_bin, axis=1))
    #figure.canvas.draw()
    #figure.canvas.flush_events()
    shape = get_shape_pos(frame)[0]
    frame = get_shape_pos(frame)[1]

    visual_layer = cv2.imread("field.png")
    
    visual_layer = cv2.rectangle(visual_layer, [290+50, shape[0]], [290+150, shape[0]+200], (0, 0, 255), -1)

    ch = 0
    for i, k in aruco[0].items():
        print(get_angle(rframe)[0], [100 + width//2 + k[1][0], k[1][1]])
        try:
            visual_layer = alt_insert_rotated_image(visual_layer, create_aruco_marker(i), get_angle(rframe)[ch], [300 + k[1][0], k[1][1]])
            visual_layer = cv2.putText(visual_layer, f'Aruco: {i}', [300 + k[1][0], k[1][1]], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 160, 0), 1, cv2.LINE_AA)
            visual_layer = cv2.putText(visual_layer, f'Map: {[300 + k[1][0], k[1][1]]}', [300 + k[1][0], k[1][1]+15], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 160, 0), 1, cv2.LINE_AA)
            rco = get_robot_coords([300 + k[1][0], k[1][1]], -400, 375, True)
            visual_layer = cv2.putText(visual_layer, f'Robot: {rco}', [300 + k[1][0], k[1][1]+30], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 160, 0), 1, cv2.LINE_AA)
        except Exception as err:
            print(err)
        ch += 1
    #for i, k in aruco[0].items():
    #    print("k:", k[1])
    #    if k[1][0] >= 70 and k[1][0] <= 510 and k[1][1] >= 70 and k[1][1] <= 310:      
    #        visual_layer = insert_rotated_image(visual_layer, aruco_img, get_angle(rframe)[0], [k[1][0], k[1][1]])
    #    else:
    #        print(f"error: {k[1][0]}, {k[1][1]}")
        #visual_layer = cv2.rectangle(visual_layer, [k[1][0]-25, k[1][1]-25], [k[1][0]+25, k[1][1]+25], (0, 0, 0), -1)


    try:
        print("get_angle", get_angle(rframe))
    except:
        pass
    #cv2.imwrite("300.png", frame)
    cv2.imshow("Main", frame)
    cv2.imshow("Visual", visual_layer)
    
    #cv2.imshow('result', get_shape_pos(frame)[2])
    key = cv2.waitKey(100) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('e'):
        cv2.imwrite("r1", frame)
        """
if __name__ == "__main__":
    while True:
        frame = get_image()
        frame = cam_correct.undistort(frame)
        try:
            frame, lframe, rframe = cut_img(frame)
            cv2.imshow("rMain", rframe)
            aruco = get_aruco_pos(rframe)
            #print(f"aruco: {aruco}")
            #aruco[0][17][1][0] += 290
        except Exception as err:
            print(err)

        print(check_(rframe))

        cv2.imshow("Main", frame)

        key = cv2.waitKey(100) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
