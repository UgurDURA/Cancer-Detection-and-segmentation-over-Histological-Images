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

rstBChan = saturations[:, :, 0]
rstGChan = saturations[:, :, 1]
rstRChan = saturations[:, :, 2]

histB, bin_edges_b = np.histogram(rstBChan)
max_b = histB.max()
min_b = histB.min()
histG, bin_edges_g = np.histogram(rstGChan)
max_g = histG.max()
min_g = histG.min()
histR, bin_edges_r = np.histogram(rstRChan)
max_r = histR.max()
min_r = histR.min()

# Normalize histogram
histB = ((histB-min_b)/(max_b-min_b))
histG = ((histG-min_g)/(max_g-min_g))
histR = ((histR-min_r)/(max_r-min_r))

# Compute the CDF
icdfB = (height*width*((np.cumsum(histB))/(sum(histB))))
icdfG = (height*width*((np.cumsum(histG))/(sum(histG))))
icdfR = (height*width*((np.cumsum(histR))/(sum(histR))))

# Rescale
icdfB = max(max(rstBChan))*icdfB
icdfG = max(max(rstGChan))*icdfG
icdfR = max(max(rstRChan))*icdfR

# Reverse
max0 = (max(np.double(icdfB)))
saturations[:, :, 0] = saturations[:, :, 0] - max0

max1 = (max(np.double(icdfG)))
saturations[:, :, 1] = saturations[:, :, 1] - max1

max2 = (max(np.double(icdfR)))
saturations[:, :, 2] = saturations[:, :, 2] - max2

rstBChan = saturations[:, :, 0]
rstGChan = saturations[:, :, 1]
rstRChan = saturations[:, :, 2]

#print(max_b)
#print()
#print(histB)
#plt.hist(rstBChan)
#plt.show()