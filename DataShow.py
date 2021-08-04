import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import os
 

images = np.load(r'D:\Software Senior Project[DATA]\fold_1\Fold 1\images\fold1\images.npy')
masks=np.load(r'D:\Software Senior Project[DATA]\fold_1\Fold 1\masks\fold1\masks.npy')
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
# plt.imshow(images[0])
# plt.imshow(masks[0])
# plt(images[0])
# plt(masks[0])


"Saving the images whichs are overplotted"


# for i in range (1):
#     plt.imshow(images[i])
#     plt.imshow(masks[i])
#     imagename='images'+str(i)+'.png'
#     plt.savefig(imagename)
    

"Check how is looks like "

plt.show()

"PS. Izbanda kodlama queyfie"