import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread('images/Kidney_2_hw.png')
height = img.shape[0]
width = img.shape[1]
channels = img.shape[2]

saturations = np.zeros((height, width, channels))
sum = np.double(img[:, :, 0]) + np.double(img[:, :, 1]) + img[:, :, 2]
mu = sum / 3

for i in range(0, channels):
    cal = np.double(img[:, :, i]) - mu
    cal = np.square(cal)
    saturations[:, :, i] = np.sqrt(cal)

rstBChan = (1-saturations[:, :, 0])
rstGChan = (1-saturations[:, :, 1])
rstRChan = (1-saturations[:, :, 2])
total = cv2.merge([np.int(rstBChan*255), np.int(rstGChan*255), np.int(rstRChan*255)])

plt.imshow(total)
plt.show()