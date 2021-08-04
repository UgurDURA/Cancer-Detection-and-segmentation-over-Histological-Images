import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import os
 

images = np.load(r'C:\Users\90534\Desktop\YBitirme\Cancer-Detection-and-segmentation-over-Histological-Images\imageExamples.npy')
masks=np.load(r'C:\Users\90534\Desktop\YBitirme\Cancer-Detection-and-segmentation-over-Histological-Images\maskExamples.npy')
images=images.astype(int)
masks=masks.astype(int)


"Data seperation (Seperated into 5 instances"

# imageExampels=[]
# maskExampels=[]

# for i in range(5):
#     imageExampels.append(images[i])
#     maskExampels.append(masks[i])

# imageExampels=np.array(imageExampels)
# maskExampels=np.array(maskExampels)
# np.save('imageExamples', imageExampels)
# np.save('maskExamples', maskExampels)



"Plotting over a graph"
#plt.imshow(images[0])
#plt.imshow(masks[0])
#plt(images[0])
#plt(masks[0])

r1,g1, b1, r2, g2, b2 = np.split(masks[0], 6, axis=2)
m1 = np.concatenate((r1,g1,b1), axis=2)
m2 = np.concatenate((r2,g2,b2), axis=2)
r3,g3,b3 = np.split(images[0],3, axis=2)
masked = np.concatenate((r3*r2*r1, g3*g2*g1, b3*g3*g1),axis=2)
plt.imshow(masked)
plt.show()

"Saving the images whichs are overplotted"

#for i in range (1):


    # imagename='images'+str(i)+'.png'
    # plt.savefig(imagename)
    

"Check how is looks like "

plt.show()

"PS. Izbanda kodlama queyfie"