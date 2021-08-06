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

npp, inf, stc, dc, epi, bg  = np.split(masks[0], 6, axis=2) #256x256 #uint8'e çevir!

img = np.asarray(images[0], dtype=np.uint8)

m1 = np.concatenate((npp,npp,npp), axis=2)
m1int = np.asarray(m1, dtype=np.uint8)

m2 = np.concatenate((inf, inf,inf),axis=2)
m2int = np.asarray(m2, dtype=np.uint8)

m3 = np.concatenate((stc,stc,stc), axis=2)
m3int = np.asarray(m3, dtype=np.uint8)

m4 = np.concatenate((dc,dc,dc), axis=2)
m4int = np.asarray(m4, dtype=np.uint8)

m5 = np.concatenate((epi,epi,epi), axis=2)
m5int = np.asarray(m5, dtype=np.uint8)

m6 = np.concatenate((bg,bg,bg), axis=2)
m6int = np.asarray(m6, dtype=np.uint8)

mmm1 = np.multiply(m1int,img)
mmm2 = np.multiply(m2int,img)
mmm3 = np.multiply(m3int,img)
mmm4 = np.multiply(m4int,img)
mmm5 = np.multiply(m5int,img)
mmm6 = np.multiply(m6int,img)

m = np.multiply(mmm1,np.multiply(mmm2,np.multiply(mmm3,np.multiply(mmm4,np.multiply(mmm5,np.multiply(mmm6,img))))))
mm = np.add(m,mmm6)

masked = np.add(mmm1,np.add(mmm2,np.add(mmm3,np.add(mmm4,np.add(mmm5,mmm6)))))

fig = plt.figure()
ax1 = fig.add_subplot(2,4,1)
ax1.imshow(np.add(mmm1,img))
plt.title("mask1")

ax2 = fig.add_subplot(2,4,2)
ax2.imshow(np.add(mmm2,img))
plt.title("mask2")

ax3 = fig.add_subplot(2,4,3)
ax3.imshow(np.add(mmm3,img))
plt.title("mask3")

ax4 = fig.add_subplot(2,4,4)
ax4.imshow(np.add(mmm4,img))
plt.title("mask4")

ax5 = fig.add_subplot(2,4,5)
ax5.imshow(np.add(mmm5,img))
plt.title("mask5")

ax6 = fig.add_subplot(2,4,6)
ax6.imshow(mmm6)
plt.title("mask6 (background)")

ax7 = fig.add_subplot(2,4,7)
ax7.imshow(mm)
plt.title("all masks in order")

ax8 = fig.add_subplot(2,4,8)
ax8.imshow(masked)
plt.title("all masks added")

fig.show()
plt.show()