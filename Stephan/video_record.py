import cv2
from camera import CameraClient

width = 640
height = 480

writer= cv2.VideoWriter('basicvideo.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
camera = CameraClient("192.168.0.222", 9988)

while True:
    frame = camera.get_frame()

    writer.write(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break



writer.release()
cv2.destroyAllWindows()
