import cv2
import cv2.aruco as aruco

def create_aruco_marker(id_, dict_id=aruco.DICT_6X6_250, size=200):
    # Выбираем словарь ArUco
    aruco_dict = aruco.Dictionary_get(dict_id)

    # Генерируем изображение маркера
    img = aruco.drawMarker(aruco_dict, id_, size)

    return img

cv2.imshow("aruco", create_aruco_marker(17))
