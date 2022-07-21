import cv2
import matplotlib.pyplot as plt


# Read image
img = cv2.imread("sendImage 5.png")
# plt.imshow(img[:,:,::-1])
# plt.show()
print(img.shape)


# Cropout OpenCV logo
img = img[450:580, 450:530]
plt.imshow(img[:,:,::-1])
plt.show()




###################################################################################################################################################
                                            #EDSR SuperResolution
###################################################################################################################################################

# sr = cv2.dnn_superres.DnnSuperResImpl_create()

# path = "SuperResolutionZoomAlgorithms/EDSR_x4.pb"

# sr.readModel(path)

# sr.setModel("edsr",4)

# result = sr.upsample(img)

# # Resized image
# resized = cv2.resize(img,dsize=None,fx=4,fy=4)


###################################################################################################################################################
                                            #ESPCN SuperResolution
###################################################################################################################################################

# sr = cv2.dnn_superres.DnnSuperResImpl_create()

# path = "SuperResolutionZoomAlgorithms/ESPCN_x3.pb"

# sr.readModel(path)

# sr.setModel("espcn",3)

# result = sr.upsample(img)

# # Resized image
# resized = cv2.resize(img,dsize=None,fx=3,fy=3)


###################################################################################################################################################
                                            #FRCNN SuperResolution (3X)
###################################################################################################################################################

sr = cv2.dnn_superres.DnnSuperResImpl_create()

path = "SuperResolutionZoomAlgorithms/FSRCNN_x3.pb"

sr.readModel(path)

sr.setModel("fsrcnn",3)

result = sr.upsample(img)

# Resized image
resized = cv2.resize(img,dsize=None,fx=3,fy=3)


###################################################################################################################################################
                                            #FRCNN SuperResolution (3X_Small) --> 3x is better not this one 
###################################################################################################################################################

# sr = cv2.dnn_superres.DnnSuperResImpl_create()

# path = "SuperResolutionZoomAlgorithms/FSRCNN-small_x3.pb"

# sr.readModel(path)

# sr.setModel("fsrcnn",3)

# result = sr.upsample(img)

# # Resized image
# resized = cv2.resize(img,dsize=None,fx=3,fy=3)


###################################################################################################################################################
                                            #LapSRN SuperResolution 
###################################################################################################################################################
# sr = cv2.dnn_superres.DnnSuperResImpl_create()

# path = "SuperResolutionZoomAlgorithms/LapSRN_x8.pb"

# sr.readModel(path)

# sr.setModel("lapsrn",8)

# result = sr.upsample(img)

# # Resized image
# resized = cv2.resize(img,dsize=None,fx=8,fy=8)


plt.figure(figsize=(12,8))
plt.subplot(1,3,1)
# Original image
plt.imshow(img[:,:,::-1])
plt.subplot(1,3,2)
# SR upscaled
plt.imshow(result[:,:,::-1])
plt.subplot(1,3,3)
# OpenCV upscaled
plt.imshow(resized[:,:,::-1])
plt.show()