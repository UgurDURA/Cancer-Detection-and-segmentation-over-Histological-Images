import cv2

def cbcr_transform(image):
    YCrCb = cv2.cvtColor(image, cv2.cv.CV_BGR2YCrCb)
    # Luminance Y
    Y = YCrCb[:, :, 0]
    # Chrominance Cr
    Cr = YCrCb[:, :, 1]
    # Chrominance Cb
    Cb = YCrCb[:, :, 2]

    return Y, Cb, Cr