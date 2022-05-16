import cv2
import numpy as np
from skimage.restoration import estimate_sigma


def non_local_means(img):  # Non local means filtering is used to remove gaussian blur in the image.
    sigma_est = np.mean(estimate_sigma(img, multichannel=True))  # get sigma values from all the channels
    denoised_img = cv2.fastNlMeansDenoisingColored(img, None, sigma_est, sigma_est, 5, 21)  # apply non local means filter
    return denoised_img