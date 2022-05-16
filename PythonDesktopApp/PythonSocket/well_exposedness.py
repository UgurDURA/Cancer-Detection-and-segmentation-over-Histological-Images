import math

import numpy as np


def well_exposedness(image):
    im_b = image[:, :, 0] 
    im_g = image[:, :, 1]
    im_r = image[:, :, 2]

    m_im_b = np.mean(im_b)  # computes the mean over all dimensions of an array. "all".
    m_im_g = np.mean(im_g)
    m_im_r = np.mean(im_r)

    std_im_b = np.std(im_b)  # computes the standard deviation over all elements of A. "all".
    std_im_g = np.std(im_g)
    std_im_r = np.std(im_r)

    result_r = math.exp(- (im_r - np.power((1 - m_im_r), 2)) / (2 * (std_im_r ^ 2)))
    result_g = math.exp(- (im_g - np.power((1 - m_im_g), 2)) / (2 * (std_im_g ^ 2)))
    result_b = math.exp(- (im_b - np.power((1 - m_im_b), 2)) / (2 * (std_im_b ^ 2)))

    r = result_r
    g = result_g
    b = result_b

    return r, g, b
