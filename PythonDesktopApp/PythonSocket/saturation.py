import cv2
import matplotlib.pyplot as plt
import numpy as np


def saturation(img):
    # img = cv2.imread('images/Kidney_2_hw.png')
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]  # get number of channels of the image

    saturations = np.zeros((height, width, channels))  # create a zero array with the same size as the input image
    # saturation is computed as the standard deviation of the color channels:
    sum = np.double(img[:, :, 0]) + np.double(img[:, :, 1]) + img[:, :, 2]
    mu = sum / 3
    for i in range(0, channels):
        cal = np.double(img[:, :, i]) - mu
        cal = np.square(cal)
        saturations[:, :, i] = np.sqrt(cal)

    rstBChan = (1 - saturations[:, :, 0])  # calculate reverse saturation of channel b
    rstGChan = (1 - saturations[:, :, 1])  # calculate reverse saturation of channel g
    rstRChan = (1 - saturations[:, :, 2])  # calculate reverse saturation of channel r
    # total = cv2.merge([np.int(rstBChan * 255), np.int(rstGChan * 255), np.int(rstRChan * 255)])
    # plt.imshow(total)
    # plt.show()
    return rstBChan, rstGChan, rstRChan
