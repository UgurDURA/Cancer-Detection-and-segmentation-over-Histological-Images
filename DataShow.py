import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import os
 

images = np.load(r'C:\Users\ugur_\OneDrive\Masaüstü\Projects\Cancer-Detection-and-segmentation-over-Histological-Images\Cancer-Detection-and-segmentation-over-Histological-Images\imageExamples.npy')
masks=np.load(r'C:\Users\ugur_\OneDrive\Masaüstü\Projects\Cancer-Detection-and-segmentation-over-Histological-Images\Cancer-Detection-and-segmentation-over-Histological-Images\maskExamples.npy')
images=images.astype(int)
masks=masks.astype(int)

# imageExampels=[]
# maskExampels=[]

# for i in range(100):
#     imageExampels.append(images[i])
#     maskExampels.append(masks[i])

# imageExampels=np.array(imageExampels)
# maskExampels=np.array(maskExampels)
# np.save('imageExamples', imageExampels)
# np.save('maskExamples', maskExampels)


# plt.imshow(images[0])
# plt.imshow(masks[0])
# plt(images[0])
# plt(masks[0])



for i in range (1):
    plt.imshow(images[i])
    plt.imshow(masks[i])
    imagename='images'+str(i)+'.png'
    plt.savefig(imagename)
    

plt.show()

