import cv2
import numpy as np

dick = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

with open('param.txt') as f:
    K = eval(f.readline())
    D = eval(f.readline())

def create_picture():
    window = np.zeros((500,1000,3), dtype='uint8')
    cv2.circle(window, (500,500), 100, (125, 125, 0), thickness=-11)
    cv2.circle(window, (500,500), 500, (20, 75, 9), thickness=1)
    #cv2.rectangle(window,(500-143), 100, (100, 300), (255,255,255), 5)
    return window


    
def crop_img(img):
    cropped_image = img[0:480, 90:550]
    return cropped_image


def undistort(img):
    DIM = img.shape[:2][::-1]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img[::]

def warp_da(frame):
    global dick
    c=[]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.aruco.detectMarkers(gray, dick)
    if res[1] is not None and (0 in res[1]) and (1 in res[1])and (2 in res[1]) and (3 in res[1]):
        for i in range(4):
            
            marker=i
            index=np.where(res[1]==marker)[0][0]
            pt0=res[0][index][0][marker].astype(np.int16)
            c.append(list(pt0))
            cv2.circle(frame, pt0, 10, (0,0,255), thickness=-1)
            
        h, w, _ = frame.shape
        input_pt=np.array(c)
        output_pt=np.array([[0,0], [w,0],[w,h],[0,h]])
        h_, _ = cv2.findHomography(input_pt, output_pt)
        np.savetxt('h_wh.txt', h_)
       

        return h_
    else:
        return np.loadtxt('h_wh.txt')
