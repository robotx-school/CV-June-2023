import cv2
def show_all(camera_image, field_img, visualizer_image):
    camera_image = cv2.resize(camera_image, (320, 240))
    field_img = cv2.resize(field_img, (320, 240))
    visualizer_image = cv2.resize(visualizer_image, (640, 480))
    visualizer_image = cv2.cvtColor(visualizer_image, cv2.COLOR_BGRA2BGR)
    top = cv2.hconcat((camera_image, field_img))
    top = cv2.resize(top, (640, 240))
    all_ = cv2.vconcat((top, visualizer_image))
    return all_
