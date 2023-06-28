import cv2
def save_image_set(image_set_dict):
    for name, image in image_set_dict.items():
        cv2.imwrite(f"images/{name}.jpg", image)
