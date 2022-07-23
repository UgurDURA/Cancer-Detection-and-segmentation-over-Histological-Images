import cv2
import numpy as np
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.exposure import match_histograms
from sklearn import preprocessing
from sklearn.decomposition import PCA

def pca_weight_char(image):

    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]  # 3

    x = np.zeros((1, height*width))
    for i in range(0, channels):
        a_channel = image[:, :, i]  # get channels 0 = B, 1 = G, 2 = R
        col = np.double(a_channel)
        col = col.flatten()
        col = col.T
        print(col)
        x = np.row_stack((x, col))# rc x N


    x = np.delete(x, 0, axis=0)
    print(x)
    weights = np.zeros((1, height*width))

    pca = PCA().fit(x)
    weights = pca.components_
    print(weights)

    PCA_Weights = np.zeros((height, width, channels))  # dimensions -> height x width x 3

    for i in range(0, channels):
        p = np.reshape(weights[i], [height, width])  # reshape each channel
        PCA_Weights[:, :, i] =(p - np.min(p))/np.ptp(p)

    min_range = 0.85
    max_range = 1

    for a in range(0, channels):
        # PCA_Weights[:, :, i] = cv2.GaussianBlur(PCA_Weights[:, :, i], (5,5), cv2.BORDER_DEFAULT)
        for i in range(0, height):
            for j in range(0, width):
                if PCA_Weights[i,j,a]>min_range and PCA_Weights[i,j,a]<max_range:
                    PCA_Weights[i,j,a] = 1

    
    
    return PCA_Weights[:, :, 0], PCA_Weights[:, :, 1], PCA_Weights[:, :, 2]


    print(PCA_Weights)
    print("PCA Weight Shape", PCA_Weights.shape())


    row, column = img.shape

 
