from dotenv import load_dotenv
import os


class Config:
    def __init__(self) -> None:
        load_dotenv()
        self.camera_ip = os.getenv('CAMERA_IP')
        self.camera_port = int(os.getenv('CAMERA_PORT'))
        self.camera_update_rate = int(os.getenv('CAMERA_UPDATE_RATE'))
        self.camera_update_rate = 1
        self.force_cache_use = bool(os.getenv('FORCE_CACHE_USE'))
        # print("Config", self.force_cache_use)
        self.force_cache_use = False
        self.homography_cache_path = os.getenv('HOMOGRAPHY_CACHE_PATH')

        # Builtin
        self.battery_marker_id = 17
