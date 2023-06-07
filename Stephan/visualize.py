import numpy as np
import cv2
import cv2.aruco as aruco
from typing import List


class Visualize:
    def __init__(self) -> None:
        self.image = cv2.imread("field_base.jpg")
        self.image = cv2.resize(self.image, (600, 400))
        # cv2.line(self.image, (22, 0), (22, 793), (20, 0, 255), 1)
        # cv2.line(self.image, (101, 0), (101, 793), (20, 0, 255), 1)
        # cv2.line(self.image, (1091, 0), (1091, 793), (20, 0, 255), 1)
        self.image = self.image[11: 11 + 378, 11: 11 + 578]
        self.image = cv2.resize(self.image, (600, 400))
        self.image_fallback = self.image.copy()
        print(self.image.shape)
        self.border_size = 200

        '''
        Field size mm:
        400 x 600
        Robot Size:
        200 x 150
        '''

    def add_border(self) -> None:
        self.image = cv2.copyMakeBorder(src=self.image, top=self.border_size, bottom=self.border_size,
                                        left=self.border_size, right=self.border_size, borderType=cv2.BORDER_CONSTANT, value=(184, 184, 184))

    def update(self):
        self.image = self.image_fallback.copy()

    def rotate_image(self, mat, angle):
        height, width = mat.shape[:2]
        image_center = (width / 2, height / 2)

        rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
        return rotated_mat

    def create_aruco_marker(self, id, dict_id=aruco.DICT_4X4_250, size=50):
        size -= 10
        aruco_dict = aruco.Dictionary_get(dict_id)
        img = aruco.drawMarker(aruco_dict, id, size)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
        img = cv2.copyMakeBorder(src=img, top=5, bottom=5,
                                 left=5, right=5, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255, 255))
        return img

    def merge_image(self, back: np.ndarray, front: np.ndarray, x: int, y: int):
        if back.shape[2] == 3:
            back = cv2.cvtColor(back, cv2.COLOR_BGR2BGRA)
        if front.shape[2] == 3:
            front = cv2.cvtColor(front, cv2.COLOR_BGR2BGRA)

        bh, bw = back.shape[:2]
        fh, fw = front.shape[:2]
        x1, x2 = max(x, 0), min(x + fw, bw)
        y1, y2 = max(y, 0), min(y + fh, bh)
        front_cropped = front[y1 - y: y2 - y, x1 - x: x2 - x]
        back_cropped = back[y1:y2, x1:x2]

        alpha_front = front_cropped[:, :, 3:4] / 255
        alpha_back = back_cropped[:, :, 3:4] / 255

        result = back.copy()

        result[y1:y2, x1:x2, :3] = alpha_front * front_cropped[:,
                                                               :, :3] + (1 - alpha_front) * back_cropped[:, :, :3]
        result[y1:y2, x1:x2, 3:4] = (
            alpha_front + alpha_back) / (1 + alpha_front*alpha_back) * 255

        return result

    def draw_marker(self, x: int, y: int, marker_id: int, angle: int) -> None:
        aruco_image = self.create_aruco_marker(marker_id)
        aruco_image = self.rotate_image(aruco_image, angle)
        new_field = self.image.copy()
        self.image = self.merge_image(new_field, aruco_image, x - 25, y - 25)

    def draw_robot(self, robot_rect: List[tuple]) -> None:
        # print(robot_rect)
        x1, y1 = robot_rect[0]
        x4, y4 = robot_rect[-1]
        x, y, w, h = x1, y1, (x4 - x1), (y4 - y1)
        sub_img = self.image[y:y+h, x:x+w]
        robot_rect = np.zeros(sub_img.shape, np.uint8)
        robot_rect[:] = (0, 0, 255)
        res = cv2.addWeighted(sub_img, 0.5, robot_rect, 0.5, 1.0)
        self.image[y:y+h, x:x+w] = res


if __name__ == "__main__":
    visualizer = Visualize()
    visualizer.draw_marker(100, 100, 17, 45)
    visualizer.add_border()

    while True:
        cv2.imshow("Visualization", visualizer.image)
        key = cv2.waitKey(0) & 0xFF
        if key == 27:
            break
