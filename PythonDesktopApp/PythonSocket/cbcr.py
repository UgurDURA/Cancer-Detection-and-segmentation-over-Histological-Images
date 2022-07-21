import cv2
import numpy as np

def cbcr_transform(image):
    image = np.asarray(image, dtype=np.uint8)
    YCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    # Luminance Y
    Y = YCrCb[:, :, 0]
    # Chrominance Cr
    Cr = YCrCb[:, :, 1]
    # Chrominance Cb
    Cb = YCrCb[:, :, 2]

    return Y, Cb, Cr