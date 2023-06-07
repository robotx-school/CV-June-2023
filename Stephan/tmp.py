
# import numpy as np
# import cv2

# # create a blank image with an alpha channel
# img = np.zeros((500, 500, 4), dtype=np.uint8)

# # set the alpha channel to fully transparent
# img[:,:,3] = 0

# # define the center point, size, and angle of the rectangle
# center = (250, 250)
# size = (200, 100)
# angle = 30

# # calculate the minimum area rectangle
# rect = cv2.minAreaRect(cv2.boxPoints((center, size, angle)))

# # find the four corners of the rectangle
# box = np.int0(cv2.boxPoints(rect))

# # define the color for the rectangle
# color = (0, 255, 0, 128) # semi-transparent green

# # fill in the rectangle with the semi-transparent color
# cv2.fillPoly(img, [box], color)

# # display the image
# cv2.imshow("Rotated Rectangle", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
import numpy as np


image = cv2.imread("field.png")
overlay = image.copy()

x, y, w, h = 194, 65, (283 - 65), 100  # Rectangle parameters
# cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 200, 0), -1)  # A filled rectangle

pts = np.array([(194, 65), (194, 283), (352, 283), (352, 65)])

cv2.fillPoly(overlay, pts=[pts], color=(0, 0, 255))

# arr = np.array()
# arr = cv2.boxPoints(((194, 65), (100, 100), 45))
# print(arr)
# rect = cv2.minAreaRect(arr)
# box = cv2.boxPoints(rect)  # cv2.boxPoints(rect) for OpenCV 3.x
# box = np.intp(box)

# cv2.drawContours(overlay, [box], 0, (0, 0, 255), thickness=-1)


alpha = 0.5  # Transparency factor.

# rect = cv2.minAreaRect(cv2.boxPoints((center, size, angle)))

# Following line overlays transparent rectangle over the image
image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

cv2.imshow("Rotated Rectangle", image_new)
cv2.waitKey(0)
cv2.destroyAllWindows()

# import cv2
# import numpy as np
# contours = np.array([[50,50], [50,150], [150,150], [150,50]])
# image = np.zeros((200,200))
# cv2.fillPoly(image, pts = [contours], color =(255,255,255))
# cv2.imshow("filledPolygon", image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
