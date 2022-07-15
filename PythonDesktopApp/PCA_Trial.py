import cv2
import numpy as np
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.exposure import match_histograms
from sklearn import preprocessing
from sklearn.decomposition import PCA

img = cv2.imread('Kidney.jpeg')  # read image

#img = img_as_float(img)
img_ref = cv2.imread('Kidney.jpeg')  # read ref image
#img_ref = img_as_float(img_ref)

#sigma_est = np.mean(estimate_sigma(img, multichannel=True))  # get sigma values from all the channels

#denoise_img = cv2.fastNlMeansDenoisingColored(img, None, sigma_est, sigma_est, 5, 21)

#matched = match_histograms(image=denoise_img, reference=img_ref, multichannel=True)

############################################################################################################################################

                                                                    #Histogram Matching Between Channels

############################################################################################################################################

#(B, G, R) = cv2.split(matched)

#outb_refb = match_histograms(image=B, reference=B, multichannel=False)
#outg_refb = match_histograms(image=G, reference=B, multichannel=False)
#outr_refb = match_histograms(image=R, reference=B, multichannel=False)

#outb_refg = match_histograms(image=B, reference=G, multichannel=False)  # Blue matched with green
#outg_refg = match_histograms(image=G, reference=G, multichannel=False)  # Green matched with green
#outr_refg = match_histograms(image=R, reference=G, multichannel=False)  # Red matched with green

#outb_refr = match_histograms(image=B, reference=R, multichannel=False)  # Blue matched with red
#outg_refr = match_histograms(image=G, reference=R, multichannel=False)  # Green matched with red
#outr_refr = match_histograms(image=R, reference=R, multichannel=False)  # Red matched with red

#out_refb = cv2.merge([outb_refb, outg_refb, outr_refb])
#out_refg = cv2.merge([outb_refg, outg_refg, outr_refg])
#out_refr = cv2.merge([outb_refr, outg_refr, outr_refr])

############################################################################################################################################

                                                                #PCA Map Extraction

############################################################################################################################################

#combined_img_for_pca = cv2.merge([out_refb, out_refg, out_refr])

#height = combined_img_for_pca.shape[0]
#width = combined_img_for_pca.shape[1]
#channels = combined_img_for_pca.shape[2]
height = img.shape[0]
width = img.shape[1]
channels = img.shape[2]  # 3

x = np.zeros((1, height*width))
for i in range(0, channels):
    a_channel = img[:, :, i]  # get channels 0 = B, 1 = G, 2 = R
    col = np.double(a_channel)
    #col = np.reshape(col, (-1, 1))  # one single column
    col = col.flatten()
    col = col.T
    print(col)
    x = np.row_stack((x, col))# rc x N

    


x = np.delete(x, 0, axis=0)
print(x)
weights = np.zeros((1, height*width))
# new_x = np.reshape(np.x, (-1, 1))
#pca = PCA(n_components=2).fit(x) # 2nd component only
pca = PCA().fit(x)
weights = pca.components_
print(weights)


#out = np.zeros((weights.shape[0], weights.shape[1]))



#print("Result of Normalization: \n", normalized)

#cv2.normalize(weights, out, 0.0, 1.0, cv2.NORM_MINMAX)
# print('normalized:')
# print(weights)

PCA_Weights = np.zeros((height, width, channels))  # dimensions -> height x width x 3

for i in range(0, channels):
    p = np.reshape(weights[i], [height, width])  # reshape each channel
    PCA_Weights[:, :, i] =(p - np.min(p))/np.ptp(p)



# for i in range(0, channels):
#     PCA_Weights[:, :, i] = cv2.GaussianBlur(PCA_Weights[:, :, i], (5,5), cv2.BORDER_DEFAULT)


print(PCA_Weights)
print("PCA Weight Shape", PCA_Weights.shape[2])
#cv2.imshow("Out_refb", out_refb)
#cv2.imshow("Original", img)
#cv2.imshow("Reference Image", img_ref)
#cv2.imshow("NLM Filtered", denoise_img)
#cv2.imshow("HM", matched)

cv2.waitKey(0)
cv2.destroyAllWindows()