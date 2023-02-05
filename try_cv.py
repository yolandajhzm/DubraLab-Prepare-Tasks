# use cv2 to get 2d numpy array of monochrome image

import cv2

imgs = cv2.imread("cat.png", cv2.IMREAD_GRAYSCALE)
print(type(imgs))

