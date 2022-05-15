import cv2
from matplotlib import pyplot as plt

rgbImage = cv2.imread('images/Kidney_2_hw.png')

#gray = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)
#img = cv2.GaussianBlur(gray, (3, 3), 0)
laplacian = cv2.Laplacian(rgbImage, cv2.CV_64F)

plt.imshow(rgbImage)
plt.imshow(laplacian)
plt.show()
