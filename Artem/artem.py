# I created a file for you :)
# Thank You! :)

import cv2
import numpy as np
import os
import glob
import struct
import pickle
import socket


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
safeCords = []


import math


def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]


def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA) ** 0.5
    magB = dot(vB, vB) ** 0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    anglee = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(anglee) % 360

    if ang_deg-180 >= 0:
        # As in if statement
        return 360 - ang_deg
    else:

        return ang_deg


def robot_cords(x_r, y_r):
    offset_x = 143
    offset_y = 200
    for cords in robot_cords:
        x_r, y_r = y_r, - x_r


def get_img():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.0.222'
    port = 9988
    client_socket.connect((host_ip, port))

    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        client_socket.close()
        return frame


def create_aruco_marker(id, dict_id=cv2.aruco.DICT_4X4_250, size=50, border_size=5):
    aruco_dict = cv2.aruco.Dictionary_get(dict_id)
    imag = cv2.aruco.drawMarker(aruco_dict, id, size)
    imag = cv2.copyMakeBorder(imag, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, None,
                              value=255)
    imag = cv2.cvtColor(imag, cv2.COLOR_GRAY2BGR)
    return imag


def insert_rotated_image(big_image, small_image, angl, center):
    if big_image.shape[2] == 3:
        big_image = cv2.cvtColor(big_image, cv2.COLOR_BGR2BGRA)
    if small_image.shape[2] == 3:
        small_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2BGRA)

    (h, w) = small_image.shape[:2]
    center_img = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center_img, angl, 1.0)
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])

    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    rotation_matrix[0, 2] += (new_w / 2) - center_img[0]
    rotation_matrix[1, 2] += (new_h / 2) - center_img[1]

    small_image = cv2.warpAffine(small_image, rotation_matrix, (new_w, new_h), flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    y, x = center
    y1, y2 = max(0, y - new_h // 2), min(big_image.shape[0], y + new_h // 2)
    x1, x2 = max(0, x - new_w // 2), min(big_image.shape[1], x + new_w // 2)

    delta_y = y2 - y1 - small_image.shape[0]
    delta_x = x2 - x1 - small_image.shape[1]

    alpha_s = small_image[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        big_image[y1:y2 - delta_y, x1:x2 - delta_x, c] = (alpha_s * small_image[:, :, c] +
                                                alpha_l * big_image[y1:y2 - delta_y, x1:x2 - delta_x, c])
    return big_image


aruco = create_aruco_marker(17)
bg_image = cv2.imread("field.jpg", cv2.IMREAD_UNCHANGED)
bg_image = cv2.resize(bg_image, (580, 380), interpolation=cv2.INTER_AREA)

new_img = insert_rotated_image(bg_image, aruco, 45, (300, 200))

cv2.imshow("aruco", new_img)


def get_hsv():
    global res_img
    hsv = cv2.cvtColor(res_img, cv2.COLOR_BGR2HSV)
    h1 = 0
    s1 = 144
    v1 = 66
    h2 = 17
    s2 = 255
    v2 = 255
    hsv_min = np.array((h1, s1, v1), np.uint8)
    hsv_max = np.array((h2, s2, v2), np.uint8)
    img_bin = cv2.inRange(hsv, hsv_min, hsv_max)
    _, contours, hierarchy = cv2.findContours(img_bin.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    corners, ids, p = cv2.aruco.detectMarkers(res_img, dictionary)
    if ids is not None:
        # Рисование контуров маркеров и центров
        cv2.aruco.drawDetectedMarkers(res_img, corners)
    for x in range(len(ids)):
        # Вычисление центра текущего маркера
        x_center = int((corners[x][0][0][0] + corners[x][0][2][0]) / 2)
        y_center = int((corners[x][0][0][1] + corners[x][0][2][1]) / 2)
        cv2.circle(res_img, (x_center, y_center), 5, (0, 255, 0), -1)
    cv2.drawContours(res_img, contours, -1, (0, 255, 0), 3, cv2.LINE_AA, hierarchy, 1)

    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    x_mm = int((380 // w) * x_center)
    y_mm = int((580 // h) * y_center)

    img_bin = img_bin.sum(axis=1)
    return img_bin


while True:
    img = get_img()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray, dictionary)

    coords = []
    if res[1] is not None and 0 in res[1] and 1 in res[1] and 2 in res[1] and 3 in res[1]:
        for marker in range(4):
            index = np.where(res[1] == marker)[0][0]
            pt0 = res[0][index][0][marker].astype(np.int16)
            coords.append(list(pt0))
            cv2.circle(img, pt0, 10, (255, 255, 255), thickness=-1)
        with open("save.coords", "wb") as f:
            np.save(f, coords)
        safeCords = coords
        height, width, _ = img.shape
        input_pt = np.array(coords)
        output_pt = np.array([[0, 0], [width, 0], [width, height], [0, height]])
        h, _ = cv2.findHomography(input_pt, output_pt)
        res_img = cv2.warpPerspective(img, h, (width, height))
        get_hsv()
        # cv2.imshow('111', res_img)
    elif res[1] is not None and safeCords is not None:
        with open("save.coords", "rb") as f:
            safeCords = np.load(f)
        for i in range(4):
            cv2.circle(img, safeCords[i], 5, (0, 255, 255), thickness=-1)
        height, width, _ = img.shape
        input_pt = np.array(safeCords)
        output_pt = np.array([[0, 0], [width, 0], [width, height], [0, height]])
        h, _ = cv2.findHomography(input_pt, output_pt)
        res_img = cv2.warpPerspective(img, h, (width, height))
        get_hsv()
    res_gray = cv2.cvtColor(res_img, cv2.COLOR_BGR2GRAY)
    res_detect = cv2.aruco.detectMarkers(res_gray, dictionary)
    coords17 = []
    if res[1] is not None and 17 in res_detect[1]:
        for marker in range(2):
            index = np.where(res_detect[1] == 17)[0][0]
            pt0 = res_detect[0][index][0][marker].astype(np.int16)
            coords17.append(list(pt0))
            cv2.circle(res_img, pt0, 4, (255, 255, 255), thickness=-1)
    angle = ang(((coords17[0]), (coords17[1])), ((0, 0), (1, 0)))
    cv2.putText(res_img, f"ang = {angle//1}", (coords17[0][0], coords17[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 255)
    synchrone = cv2.hconcat([img, res_img])
    # cv2.imshow('111', res_img)
    # cv2.imshow('img', img)
    cv2.imshow('syncrone', synchrone)
    # default = cv2.imread('field.jpg')
    # default = cv2.resize(default, (580, 380), interpolation=cv2.INTER_AREA)
    # print(default.shape)
    # print(new_img.shape)
    # print(img.shape)
    # print(res_img.shape)
    # pole = cv2.hconcat([default, new_img])
    # total = cv2.vconcat([synchrone, pole])
    # cv2.imshow('all', total)
    if cv2.waitKey(5) == 27:
        break
    cv2.waitKey(100)
