from camera import CameraClient
from config import Config
import cv2
import time
import numpy as np
import logging
from field import Field
from visualize import Visualize
from manipulator import UR3Client

logging.basicConfig(level=logging.INFO)
# Runtime globals
PREDEFINED_CACHE_HOMOGRAPHY = []
FORCE_HOMOGRAPHY_CACHE = False


if __name__ == "__main__":
    config = Config()
    # Initalize two UR3 robots
    manipulator_discharged = UR3Client("discharged")
    manipulator_discharged.home()
    manipulator_discharged.cube_static()
    # time.sleep(100)
    # manipulator_right = UR3Client()

    FORCE_HOMOGRAPHY_CACHE = config.force_cache_use

    if config.homography_cache_path:
        try:
            PREDEFINED_CACHE_HOMOGRAPHY = np.loadtxt(
                config.homography_cache_path)
            logging.info(f"Loaded homography: {PREDEFINED_CACHE_HOMOGRAPHY}")
        except FileNotFoundError:
            logging.warning(
                f"Can't load file {config.homography_cache_path}; No such file")
    camera = CameraClient(config.camera_ip, config.camera_port, False)
    
    field = Field(camera.K, camera.D)

    visualize = Visualize()

    while True:
        frame = camera.get_frame()
        field.update(frame, PREDEFINED_CACHE_HOMOGRAPHY.copy(),
                     FORCE_HOMOGRAPHY_CACHE, config.battery_marker_id)
        visualize.update()  # Clear image of visualization field (delete all drawed objects)

        for zone in field.robots:
            robot = field.robots[zone]
            if robot:
                visualize.draw_robot(
                    list(map(lambda coords: field.px_to_mm(*coords), robot.bounding_rect_px)))

        for zone in field.batteries:
            battery = field.batteries[zone]
            if battery:
                visualize.draw_marker(
                    *battery.px_coordinates, config.battery_marker_id, battery.rotation_degree)

        try:
            # cv2.imshow("View of field", field.image)
            # cv2.imshow("Thresh", field.thresh)
            cv2.imshow("Image", field.image)
            cv2.imshow("Visualize", visualize.image)
        except cv2.error:
            logging.error("Empty frame")

        key = cv2.waitKey(config.camera_update_rate) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):  # Save frame
            cv2.imwrite(f"./base/{time.time()}.jpg", field.image)
            logging.info("Frame saved")

        elif key == ord('c'):  # Cache homography
            logging.info("Save cache homography")
            logging.info(PREDEFINED_CACHE_HOMOGRAPHY)
            PREDEFINED_CACHE_HOMOGRAPHY = field.homography
            logging.info(PREDEFINED_CACHE_HOMOGRAPHY)
            np.savetxt(f"./homographies/{time.time()}.txt",
                       PREDEFINED_CACHE_HOMOGRAPHY)

        elif key == ord('f'):  # Toggle force homography cache usage
            if FORCE_HOMOGRAPHY_CACHE:
                FORCE_HOMOGRAPHY_CACHE = False
            else:
                FORCE_HOMOGRAPHY_CACHE = True
            logging.info(f"New cache state: {FORCE_HOMOGRAPHY_CACHE}")

        elif key == ord('e'):  # Start task execution
            logging.info("Starting task execution")
            for robot in field.robots:
                if field.robots[robot]:
                    logging.info(field.robots[robot])

            for battery in field.batteries:
                if field.batteries[battery]:
                    logging.info(field.batteries[battery])
                    logging.info(manipulator_discharged.get_robot_coords(field.batteries[battery].mm_coordinates))
        elif key == ord('b'):
            # Simulate changing battery
            pass

    # Safe exit && cleanup
    camera.close()
