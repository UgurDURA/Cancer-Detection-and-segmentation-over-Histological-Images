from cmath import exp
import math

import numpy as np


def well_exposedness(image):


    
    im_b = image[:, :, 0]  # get b channel
    im_g = image[:, :, 1]  # get g channel
    im_r = image[:, :, 2]  # get r channel

    m_im_b = np.mean(im_b)  # computes the mean over all dimensions of an array. "all".
    m_im_g = np.mean(im_g)
    m_im_r = np.mean(im_r)

    std_im_b = np.std(im_b)  # computes the standard deviation over all elements of A. "all".
    std_im_g = np.std(im_g)
    std_im_r = np.std(im_r)

    result_b = np.exp(- (im_b - np.power((1 - m_im_b), 2)) / (2 * (std_im_b ** 2)))
    result_g = np.exp(- (im_g - np.power((1 - m_im_g), 2)) / (2 * (std_im_g ** 2)))
    result_r = np.exp(- (im_r - np.power((1 - m_im_r), 2)) / (2 * (std_im_r ** 2)))

    b = 1-result_b
    g = 1-result_g
    r = 1-result_r

    print("Well Exposedness Normalization Results --------------->>>>>>>>")
    print(np.max(b))
    print(np.max(g))
    print(np.max(r))
    


    return b, g, r

# WE Maps
# Channels are recalculated to give a higher
# weight to the best-illuminated pixels.
