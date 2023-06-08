import numpy as np
import cv2
from get_field import get_field
import math
from battery import Battery
from robot import Robot
import logging


class Field:
    def __init__(self, K: np.ndarray, D: np.ndarray) -> None:
        '''
        Field object stores:
        # TODO docs
        '''
        self.image = None
        self.found_markers = None
        self.robot_hsv_min = np.array((0, 140, 173), np.uint8)
        self.robot_hsv_max = np.array((255, 255, 255), np.uint8)
        self.K = K  # camera matrix coeff
        self.D = D  # camera distortion coeff
        self.aruco_dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_250)

        # New
        self.robots = {
            "left_zone": None,
            "right_zone": None
        }  # Store all robots in field
        self.batteries = {
            "discharged_0": None,
            "discharged_1": None,
            "charged_0": None,
            "charged_1": None,
            "left_zone": None,  # Robot left zone
            "right_zone": None  # Robot right zone
        }  # Store all batteries in field

    def px_to_mm(self, x, y):
        height, width, _ = self.image.shape
        x_mm = int((600 / width) * x)
        y_mm = int((400 / height) * y)
        return (x_mm, y_mm)

    def find_batteries(self, battery_marker_id: int):
        located_batteries = {
            "discharged_0": None,
            "discharged_1": None,
            "charged_0": None,
            "charged_1": None,
            "left_zone": None,
            "right_zone": None
        }
        zones = []
        if self.found_markers:
            for i in range(len(self.found_markers[1])):
                if self.found_markers[1][i] == battery_marker_id:
                    c = self.found_markers[0][i]
                    M = cv2.moments(c)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # if cY <= 230:
                    #     cY *= 1.1
                    # else:
                    #     cY *= 0.9
                    center_px = (cX, int(cY))
                    center_mm = self.px_to_mm(*center_px)
                    x1, y1, x2, y2, x3, y3, x4, y4 = c.flatten()
                    rotation_radians = math.atan((x1 - x4) / (y4 - y1))
                    rotation_degrees = rotation_radians * (180 / math.pi)
                    if rotation_degrees > 90:
                        rotation_degrees += 180
                    rotation_degrees = abs(rotation_degrees)
                    zone = ["left_zone", "right_zone"][center_px[0] > 320]
                    if 97 <= center_px[0] <= 321:
                        zone = "left_zone"
                    elif 319 < center_px[0] <= 545:
                        zone = "right_zone"
                    elif center_px[0] < 97:  # discharged zone
                        if center_px[1] <= 240:
                            zone = "discharged_0"
                        else:
                            zone = "discharged_1"
                    elif center_px[0] > 544:  # charged zone
                        if center_px[1] <= 240:
                            zone = "charged_0"
                        else:
                            zone = "charged_1"

                    located_batteries[zone] = Battery(
                        center_px, center_mm, zone, rotation_degrees, c)
                    zones.append(zone)

        for zone in self.batteries:
            zone_detected = zone in zones
            # if zone have filled, but now - not
            if self.batteries[zone] and not zone_detected:
                self.batteries[zone] = False  # clear zone
            if zone_detected:
                self.batteries[zone] = located_batteries[zone]

    def update(self, image: np.ndarray, cache_homography: np.ndarray, use_cache: bool, battery_marker_id: int) -> None:
        '''
        Update current field information, such as:
        current_image: warped correct vertical view of field
        markers_detected: list of all detected aruco markers and their coordinates
        '''
        # TODO Only for debug puprposes
        # if True:
        #     _, self.image, self.homography = get_field(
        #         image, use_cache, cache_homography)
        # else:
        #     # Debug image
        #     _, self.image, self.homography = None, cv2.imread(
        #         "1685952769.873377.jpg"), None

        _, self.image, self.homography = get_field(
            image, use_cache, cache_homography)
        
        # self.image = cv2.flip(self.image, 1)

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.found_markers = cv2.aruco.detectMarkers(
            gray, self.aruco_dictionary)

        # self.correct_area_image = self.image
        # self.aruco_corners = self.found_markers[0]
        # self.aruco_ids = self.found_markers[1]
        self.thresh = None
        try:
            hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            thresh = cv2.inRange(
                hsv, self.robot_hsv_min, self.robot_hsv_max)
            kernel = np.ones((5, 5), 'uint8')
            thresh = cv2.erode(thresh, kernel, iterations=4)
            self.thresh = cv2.dilate(thresh, kernel, iterations=3)
            self.robot_masked_hor = np.sum(self.thresh, axis=1)
            self.robot_masked_vert = np.sum(self.thresh, axis=0)
            correct_ids = []
            for i in range(len(self.robot_masked_hor)):
                if self.robot_masked_hor[i] > 0:
                    correct_ids.append(i)

            if len(correct_ids) > 20:  # Found robot
                robot_top_y = correct_ids[0]
                robot_bottom_y = correct_ids[-1]

                cv2.line(self.image, (0, robot_top_y), (640, robot_top_y),
                         (255, 255, 0), thickness=1)
                cv2.line(self.image, (0, robot_bottom_y), (640, robot_bottom_y),
                         (255, 255, 0), thickness=1)
                correct_ids = []

                for i in range(len(self.robot_masked_vert)):
                    if self.robot_masked_vert[i] > 0:
                        correct_ids.append(i)

                robot_left_x = correct_ids[0]
                robot_right_x = correct_ids[-1]

                cv2.line(
                    self.image, (robot_left_x, 480), (robot_left_x, 0), (255, 0, 0), thickness=1)
                cv2.line(self.image, (robot_right_x, 480),
                         (robot_right_x, 0), (255, 0, 0), thickness=1)

                robot_rect = [(robot_left_x, robot_top_y), (robot_left_x, robot_bottom_y),
                              (robot_right_x, robot_top_y), (robot_right_x, robot_bottom_y)]
                self.find_batteries(battery_marker_id)
                zone = ["left_zone", "right_zone"][robot_left_x > 320]
                # Clear robot
                if self.robots["left_zone"] and zone == "right_zone":
                    self.robots["left_zone"] = None
                if self.robots["right_zone"] and zone == "left_zone":
                    self.robots["right_zone"] = None

                if not self.robots[zone]:  # New robot detected
                    logging.info("New robot detected")
                    self.robots[zone] = Robot(zone, robot_rect)
                else:  # TODO Check robot static
                    # print("Old robot")
                    x1, y1 = self.robots[zone].get_center()
                    self.robots[zone].bounding_rect_px = robot_rect.copy()
                    x2, y2 = self.robots[zone].get_center()
                    delta = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    if delta < 2:
                        # Prevent overflow for long sessions
                        if self.robots[zone].statis_frames_count <= 40:
                            self.robots[zone].statis_frames_count += 1
                    else:
                        self.robots[zone].statis_frames_count = 0
                    # print(self.robots[zone].statis_frames_count)

            else:
                self.robots["left_zone"] = None
                self.robots["right_zone"] = None

                # new_robot = True
                # for robot in self.robots:
                #     if robot.zone == zone:
                #         new_robot = False
                #         break
                # if new_robot:
                #     self.robots.append(
                #         Robot(zone, robot_rect))
                # else:  # TODO Check that robot is static
                #    pass
            # Field zones

            # Left zone
            cv2.line(self.image, (96, 0), (96, 480),
                     (0, 255, 0), thickness=2)
            cv2.line(self.image, (320, 0), (320, 480),
                     (0, 255, 0), thickness=2)
            cv2.line(self.image, (543, 0), (543, 480),
                     (0, 255, 0), thickness=2)

            # cv2.circle(self.image, self.battery_center, 1, (0, 0, 255), 2)

            # self.battery_in_robot = self.robot_top_y <= self.battery_center[
            #    1] <= self.robot_bottom_y
            # print(self.battery_center[1])

        except Exception as e:
            print(e)
