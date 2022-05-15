import numpy as np


def cdf(input_im):
    L = 256  # number of  gray levels in the image(8 - bits)
    h1 = np.zeros(1, L)
    rows = input_im.shape[0]
    cols = input_im.shape[1]

    for i in range(0, rows):
        for j in range(1, cols):
            p1 = input_im[i, j]
            h1[p1 + 1] = h1[p1 + 1] + 1

    M = rows * cols
    pdf = np.divide(h1, M)  # element wise divison.

    cdf = np.zeros(1, L)

    for i in range(1, L):
        cdf[i] = sum(pdf[1:i])
    y = cdf
    return y
