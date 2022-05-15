import cv2
import numpy as np
from sklearn.decomposition import PCA


def pca_weight_characterization(imgs):
    # >>> print img.shape
    # (342, 548, 3)

    height = imgs.shape[0]
    width = imgs.shape[1]
    channels = imgs.shape[2]

    x = []

    for i in range(0, channels):
        I = imgs[:, :, i]  #
        col = np.double(I[:])  # rc x 1
        x = np.column_stack(x, col)  # rc x N

    # new_x = np.reshape(np.x, (-1, 1)) # one single column
    pca = PCA(n_components=2)
    pca_score = pca.fit_transform(x)

    out = np.zeros(pca_score.shape, np.double)
    normalized = cv2.normalize(pca_score, out, 1.0, 0.0, cv2.NORM_MINMAX)

    PCA_Weights = np.zeros(height, width, channels)

    for i in range(0, channels):
        p = np.reshape(normalized[:, i], [height, width])
        # PCA_Weights[:,:,i] =  mat2gray(p)

    for i in range(0, channels):
        PCA_Weights[:, :, i] = cv2.GaussianBlur(PCA_Weights[:, :, i], 5)

