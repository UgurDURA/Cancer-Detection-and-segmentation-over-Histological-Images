import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import os
import cv2
import argparse
 

images = np.load(r'C:\Users\90534\Desktop\YBitirme\Cancer-Detection-and-segmentation-over-Histological-Images\imageExamples.npy')
masks=np.load(r'C:\Users\90534\Desktop\YBitirme\Cancer-Detection-and-segmentation-over-Histological-Images\maskExamples.npy')
images=images.astype(int)
masks=masks.astype(int)

"Plotting over a graph"
#plt.imshow(images[0])
#plt.imshow(masks[0])
#plt(images[0])
#plt(masks[0])

npp, inf, stc, dc, epi, bg  = np.split(masks[0], 6, axis=2) #256x256
m1 = cv2.merge([npp,npp,npp])
m2 = cv2.merge([inf, inf,inf])
m3 = np.concatenate((stc,stc,stc), axis=2)
m4 = np.concatenate((dc,dc,dc), axis=2)
m5 = np.concatenate((epi,epi,epi), axis=2)
m6 = np.concatenate((bg,bg,bg), axis=2)
r, g, b = np.split(images[0], 3 , axis=2)
newimage = cv2.merge([r, g, b])
masked = cv2.bitwise_and(newimage, m1)
cv2.imshow("masked", newimage)
cv2.waitKey()

"Saving the images whichs are overplotted"

#for i in range (1):


    # imagename='images'+str(i)+'.png'
    # plt.savefig(imagename)
    

"Check how is looks like "
