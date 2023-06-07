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

def split_two_parts(img):
    left = img[0:480,0:320]
    right = img[0:480,320:640]
    return right, left

def split_right_1(right):
    right1 = right[0:480,220:320]
    left1 = right[0:480,0:220]
    #cv2.imshow("le1ft", left1)
    right11 = right1[0:240]
    right12 = right1[240:480]
    #cv2.imshow("ri11ght", right11)
    #cv2.imshow("ri12ght", right12)
    return left1, right11, right12

def split_left_1(right):
    right1 = right[0:480,100:320]
    left1 = right[0:480,0:100]
    #cv2.imshow("le1ft", left1)
    #cv2.imshow("ri1ght", right1)
    right11 = left1[240:480]
    right12 = left1[0:240]
    # cv2.imshow("ri11ght", right11)
    # cv2.imshow("ri12ght", right12)
    return right1, right11, right12

def cutter(res):
    right, left = split_two_parts(res)
    rl, rd, ru = split_right_1(right)
    lr, ld, lu = split_left_1(left)
    return rl, rd, ru, lr, ld, lu


if __name__ == "__main__":
    while True: 
        img = serch_countr_aruko(undistort(get_image()))
        cv2.imshow("img", img)
        rl, rd, ru, lr, ld, lu = cutter(img)
        # cv2.imshow("rl", rl)
        # cv2.imshow("rd", rd)
        # cv2.imshow("ru", ru)
        # cv2.imshow("lr", lr)
        # cv2.imshow("ld", ld)
        # cv2.imshow("lu", lu)
        key = cv2.waitKey(333)
        if key == 27:
            break