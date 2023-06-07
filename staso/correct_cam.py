import cv2
import numpy as np
import os
import glob
import socket
import pickle
import struct
import time
import random
import threading
from cuter import cutter
from aruco_angle import find_aruco_rotation

dicrionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)

with open('param.txt') as f:
    K = eval(f.readline())
    D = eval(f.readline())

def undistort(img):
    global K, D
    DIM = img.shape[:2][::-1]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img[::]

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

def serch_countr_aruko(img):
    global dicrionary
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray, dicrionary)

    print(res[1])

    coords = []
    if res[1] is not None and 0 in res[1] and 1 in res[1] and 2 in res[1] and 3 in res[1]:
        for marker in range(4):
            index = np.where(res[1] == marker)[0][0]
            pt0 = res[0][index][0][marker].astype(np.int16)
            print(list(pt0), index)
            coords.append(list(pt0))
        height, width, _ = img.shape
        input_pt = np.array(coords)
        output_pt = np.array([[0, 0], [width, 0], [width, height], [0, height]])
        h, _ = cv2.findHomography(input_pt, output_pt)
        res_img = cv2.warpPerspective(img, h, (width, height))
        #print(coords)
        with open("save.cord", "wb") as f:
            np.save(f, coords)
    else:
        with open("save.cord", "rb") as f:
            coords = np.load(f)
        height, width, _ = img.shape
        input_pt = np.array(coords)
        output_pt = np.array([[0, 0], [width, 0], [width, height], [0, height]])
        #print(coords, input_pt, output_pt)
        h, _ = cv2.findHomography(input_pt, output_pt)
        res_img = cv2.warpPerspective(img, h, (width, height))

    return res_img

def hsv_corr(img):
    h,w,_=img.shape
    #img=cv2.resize(img,(w//5,h//5))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
 
    # считываем значения бегунков
    h1 = 0
    s1 = 127
    v1 = 172
    h2 = 17
    s2 = 255
    v2 = 255
    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
    img_bin1 = cv2.inRange(hsv, h_min, h_max)
    _, contours, hierarchy = cv2.findContours(img_bin1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3, cv2.LINE_AA, hierarchy, 1)
    return img_bin1, img

def robot_finder(bin_img, img):
    bin_img = bin_img.sum(axis=1)
    r = []
    for i in range(len(bin_img)):
        if i != 0 and i != (len(bin_img) - 1):
            #print(23332)
            bef = int(bin_img[i-1])
            sec = int(bin_img[i])
            af = int(bin_img[i+1])
            if sec>10000 and bef<10000 and af > 10000:
                print(sec, bef, type(sec))
                #print(sec)
                cv2.line(img, (0, i), (640, i), (0, 50, 200), 3)
                #print(374)
                r.append(i)
            elif sec>10000 and af<10000 and bef < 10000:
                print(sec, bef, type(sec))
                #print(sec)
                cv2.line(img, (0, i), (640, i), (0, 255, 200), 3)
                #print(374)
                r.append(i)
    if r == []:
        r = [0, 0]
    return img, r,bin_img

def serch_17_aruko(img):
    global dicrionary
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray, dicrionary)

    #print(res[0])
    x1 = 0
    y1 = 0
    coords17 = []
    if res[1] is not None and 17 in res[1]:
        for marker in range(4):
            index = np.where(res[1] == 17)[0][0]
            pt0 = res[0][index][0][marker].astype(np.int16)
            print(list(pt0), index)
            cv2.circle(img, pt0,5,(50,255,marker*10), 3)
            x1 += pt0[0]/4
            y1 += pt0[1]/4
        x1 = int(x1)
        y1 = int(y1)
        m = [x1,y1]
        coords17.append(m)
        cv2.circle(img, m,5,(50,255,250), 3)
    return img, m

while True:
    ti = time.time()
    #& 0xFF
    frame = get_image()
    frame = undistort(frame)
    res = serch_countr_aruko(frame)
    rl, rd, ru, lr, ld, lu = cutter(res)

    jf = [rl, rd, ru, lr, ld, lu]

    resi = []
    for k in jf:
        rot, x,y = find_aruco_rotation(k)
        print(rot, x, y)
        if rot != None:
            resi.append([rot, x,y])

        else:
            resi.append(None)
        rot, x, y = None, None, None
    print(resi)

    imr, rl = hsv_corr(rl)
    iml, lr = hsv_corr(lr)



    cv2.imshow("imrbin", imr)
    cv2.imshow("imlbin", iml)

    cv2.imshow("br", imr)
    cv2.imshow("bl", iml)

    #rot = find_aruco_rotation(res)
    #print(rot)
    imr, cordr, br = robot_finder(imr, rl)
    iml, cordl, bl = robot_finder(iml, lr)
    #res, cords17 = serch_17_aruko(res)

    cv2.imshow("imr", imr)
    cv2.imshow("iml", iml)

    key = cv2.waitKey(333)
    if key == 27:
        break
    r = time.time() - ti
    print(r)
#time.sleep(100)
cv2.destroyAllWindows()