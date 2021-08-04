import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import os
 

images = np.load(r'Images\images.npy')
masks=np.load(r'Masks\masks.npy')
images=images.astype(int)
print(images.shape)
print(images[0].shape)
print(images[1].shape)
print(images[0][1].shape)


plt.imshow(images[0])
plt(masks[0])
plt.show()


# for i in range (100):
#     plt.imshow(images[i])
#     plt(masks[i])
#     imagename='images'+str(i)+'.png'
#     plt.savefig(imagename)
    


image1 = images[0]

plt.show()

