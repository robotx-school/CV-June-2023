import cv2
import numpy as np

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)


def line_intersect(x1_1, y1_2, x1_3, y1_4, x2_1, y2_2, x2_3, y2_4):
    if x1_1 == x1_3:
        x1_1 += 0.0001
    k1 = (y1_2 - y1_4) / (x1_1 - x1_3)
    b1 = y1_4 - k1 * x1_3
    if x2_1 == x2_3:
        x2_1 += 0.0001
    k2 = (y2_2 - y2_4) / (x2_1 - x2_3)
    b2 = y2_4 - k2*x2_3
    x = (b2 - b1) / (k1 - k2)
    y = k1 * x + b1
    return x, y


def get_lost_point(marker, res):
    if marker == 0:
        index = np.where(res[1] == 1)[0][0]
        x1_1 = res[0][index][0][0][0].astype(np.int16)
        y1_2 = res[0][index][0][0][1].astype(np.int16)
        x1_3 = res[0][index][0][1][0].astype(np.int16)
        y1_4 = res[0][index][0][1][1].astype(np.int16)
        index = np.where(res[1] == 3)[0][0]
        x2_1 = res[0][index][0][0][0].astype(np.int16)
        y2_2 = res[0][index][0][0][1].astype(np.int16)
        x2_3 = res[0][index][0][3][0].astype(np.int16)
        y2_4 = res[0][index][0][3][1].astype(np.int16)
    if marker == 1:
        index = np.where(res[1] == 0)[0][0]
        x1_1 = res[0][index][0][0][0].astype(np.int16)
        y1_2 = res[0][index][0][0][1].astype(np.int16)
        x1_3 = res[0][index][0][1][0].astype(np.int16)
        y1_4 = res[0][index][0][1][1].astype(np.int16)
        index = np.where(res[1] == 2)[0][0]
        x2_1 = res[0][index][0][1][0].astype(np.int16)
        y2_2 = res[0][index][0][1][1].astype(np.int16)
        x2_3 = res[0][index][0][2][0].astype(np.int16)
        y2_4 = res[0][index][0][2][1].astype(np.int16)
    if marker == 2:
        index = np.where(res[1] == 1)[0][0]
        x1_1 = res[0][index][0][1][0].astype(np.int16)
        y1_2 = res[0][index][0][1][1].astype(np.int16)
        x1_3 = res[0][index][0][2][0].astype(np.int16)
        y1_4 = res[0][index][0][2][1].astype(np.int16)
        index = np.where(res[1] == 3)[0][0]
        x2_1 = res[0][index][0][2][0].astype(np.int16)
        y2_2 = res[0][index][0][2][1].astype(np.int16)
        x2_3 = res[0][index][0][3][0].astype(np.int16)
        y2_4 = res[0][index][0][3][1].astype(np.int16)
    if marker == 3:
        index = np.where(res[1] == 0)[0][0]
        x1_1 = res[0][index][0][0][0].astype(np.int16)
        y1_2 = res[0][index][0][0][1].astype(np.int16)
        x1_3 = res[0][index][0][3][0].astype(np.int16)
        y1_4 = res[0][index][0][3][1].astype(np.int16)
        index = np.where(res[1] == 2)[0][0]
        x2_1 = res[0][index][0][2][0].astype(np.int16)
        y2_2 = res[0][index][0][2][1].astype(np.int16)
        x2_3 = res[0][index][0][3][0].astype(np.int16)
        y2_4 = res[0][index][0][3][1].astype(np.int16)
    if marker in [0, 1, 2, 3]:
        return line_intersect(x1_1, y1_2, x1_3, y1_4, x2_1, y2_2, x2_3, y2_4)
    else:
        return None


def get_field(image, use_ready_homography=False, ready_homography=None) -> list:
    found_markers_ids = []
    if not use_ready_homography:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        res = cv2.aruco.detectMarkers(gray, dictionary)
        coords = []
        height, width, _ = image.shape
        if res[1] is not None and 3 <= len(res[1]):
            for marker in range(4):
                found_markers_ids.append(marker)
                if marker in res[1]:
                    index = np.where(res[1] == marker)[0][0]
                    pt0 = res[0][index][0][marker].astype(np.int16)
                    coords.append(list(pt0))
                else:
                    coords.append(get_lost_point(marker, res))
            input_pt = np.array(coords)
            output_pt = np.array(
                [[0, 0], [width, 0], [width, height], [0, height]])
            h, _ = cv2.findHomography(input_pt, output_pt)
            res_img = cv2.warpPerspective(image, h, (width, height))
            return [True, res_img, h]
        return [False, None, None]
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        res = cv2.aruco.detectMarkers(gray, dictionary)
        height, width, _ = image.shape
        res_img = cv2.warpPerspective(image, ready_homography, (width, height))
        return [True, res_img, ready_homography]
