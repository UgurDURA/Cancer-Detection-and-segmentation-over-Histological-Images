from email.mime import base
from operator import le
import socket
import struct
from PIL import Image
import io
import base64
import PIL
import numpy as np
import cv2 as cv2
import binascii
import struct
from PIL import ImageFile

from PythonDesktopApp.PythonSocket.cbcr import cbcr_transform
from PythonDesktopApp.PythonSocket.well_exposedness import well_exposedness

ImageFile.LOAD_TRUNCATED_IMAGES = True
import matplotlib.pyplot as plt
import pca_last

from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.exposure import match_histograms
from sklearn.decomposition import PCA
import non_local_means_filter
import histogram_matching
import math


HOST = "192.168.2.164"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
opencvImage = np.zeros



print('SERVER STARTED RUNNING')


while True:
    
    client, address = s.accept()



    data = b''  # recv() does return bytes
    counter = 0
    while True:
        try:
            print(f'data received {counter}')
            chunk = client.recv(4096)  # some 2^n number
            if not chunk:  # chunk == ''
                break

            data += chunk
            counter += 1

        except socket.error:
            client.close()
            break



    print('Packet Received')
 
    imgReceived= Image.open(io.BytesIO(data))
    # img = imgReceived.save("SendImage.png")
    # opencvImage = cv2.imread("SendImage.png")
    opencvImage = cv2.cvtColor(np.array(imgReceived), cv2.COLOR_RGB2BGR)
    
    opencvImage = cv2.rotate(opencvImage, cv2.ROTATE_90_CLOCKWISE)
    opencvImage = cv2.resize(opencvImage,(750, 1000))
    win_name = 'Send Image'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(win_name, 0, 0 )
    cv2.imshow(win_name, opencvImage)
    cv2.resizeWindow(win_name, 750, 1000)
    cv2.waitKey(0); cv2.destroyAllWindows()
    cv2.waitKey(1)
    client.close()
    break
s.close()

############################################################################################################################################

                                                                            #Receive the input
                                                                            
############################################################################################################################################

img = opencvImage
img_ref = cv2.imread("SendImage.png")

############################################################################################################################################
                                                                           
                                                                            #Non Local Means Filtering 

############################################################################################################################################

sigma_est = np.mean(estimate_sigma(img, multichannel=True))  # get sigma values from all the channels

denoise_img = cv2.fastNlMeansDenoisingColored(img, None, sigma_est, sigma_est, 5, 21)


############################################################################################################################################

                                                                            #Histogram Matching 

############################################################################################################################################

matched = match_histograms(image=denoise_img, reference=img_ref, multichannel=True)

(B, G, R) = cv2.split(matched)

BB = match_histograms(image=B, reference=B, multichannel=False)
GB = match_histograms(image=G, reference=B, multichannel=False)
RB = match_histograms(image=R, reference=B, multichannel=False)

BG = match_histograms(image=B, reference=G, multichannel=False)  # Blue matched with green
GG = match_histograms(image=G, reference=G, multichannel=False)  # Green matched with green
RG = match_histograms(image=R, reference=G, multichannel=False)  # Red matched with green

BR = match_histograms(image=B, reference=R, multichannel=False)  # Blue matched with red
GR = match_histograms(image=G, reference=R, multichannel=False)  # Green matched with red
RR = match_histograms(image=R, reference=R, multichannel=False)  # Red matched with red


############################################################################################################################################

                                                                    #Histogram Matching Between Channels

############################################################################################################################################


out_refb = cv2.merge([BB, GB, RB])
out_refg = cv2.merge([BG, GG, RG])
out_refr = cv2.merge([BR, GR, RR])
print(BB.shape)


############################################################################################################################################

                                                                #PCA Map Extraction

############################################################################################################################################


PBB, PBG, PBR = pca_last.pca_weight_char(out_refb)
PGB, PGG, PGR = pca_last.pca_weight_char(out_refg)
PRB, PRG, PRR = pca_last.pca_weight_char(out_refr)



############################################################################################################################################

                                                                #Well Exposedness Map Extraction

############################################################################################################################################


EBB, EBG, EBR = well_exposedness(out_refb)
EGB, EGG, EGR = well_exposedness(out_refg)
ERB, ERG, ERR = well_exposedness(out_refr)

############################################################################################################################################

                                                                #Brightness Map Extraction

############################################################################################################################################


DBB, DBG, DBR = well_exposedness(out_refb)
DGB, DGG, DGR = well_exposedness(out_refg)
DRB, DRG, DRR = well_exposedness(out_refr)

############################################################################################################################################

                                                                #Weight calculations

############################################################################################################################################

WBB = cv2.Laplacian(PBB * EBB * DBB)
WGB = cv2.Laplacian(PGB * EGB * DBB)
WRB = cv2.Laplacian(PRB * ERB * DRB)

WBG = cv2.Laplacian(PBG * EBG * DBG)
WGG = cv2.Laplacian(PGG * EGG * DGG)
WRG = cv2.Laplacian(PRG * ERG * DRG)

WBR = cv2.Laplacian(PBR * EBR * DBR)
WGR = cv2.Laplacian(PGR * EGR * DGR)
WRR = cv2.Laplacian(PRR * ERR * DRR)

############################################################################################################################################

                                                                #Reconstructing the Color Channels

############################################################################################################################################

recons_B = ((RB * WRB) + (GB * WGB) + (BB * WBB)) / (WRB + WGB + WBB)
recons_G = ((RG * WRG) + (GG * WGG) + (BG * WBG)) / (WRG + WGG + WBG)
recons_R = ((RR * WRR) + (GR * WGR) + (BR * WBR)) / (WRR + WGR + WBR)

final_image = cv2.merge([recons_B, recons_G, recons_R])

Cb, Cr = cbcr_transform(final_image)
refCb, refCr = cbcr_transform(img_ref)

############################################################################################################################################

                                                                #Display Each Result

############################################################################################################################################

win_name = 'Original Image'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0)
cv2.imshow(win_name, img)
cv2.resizeWindow(win_name, 750, 1000)
cv2.imshow("Original", img)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)

win_name = 'NLM Filtered'
img = cv2.rotate(denoise_img, cv2.ROTATE_90_CLOCKWISE)
img = cv2.resize(denoise_img,(750,1000))
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0 )
cv2.imshow(win_name, denoise_img)
cv2.resizeWindow(win_name, 750, 1000)
cv2.imshow("NLM Filtered", denoise_img)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)

win_name = 'HM'
img = cv2.rotate(matched, cv2.ROTATE_90_CLOCKWISE)
img = cv2.resize(matched,(750,1000))
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0 )
cv2.imshow(win_name, matched)
cv2.resizeWindow(win_name, 750, 1000)
cv2.imshow("HM", matched)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)

win_name = 'Blue Channel Matched'
img = cv2.rotate(out_refb, cv2.ROTATE_90_CLOCKWISE)
img = cv2.resize(out_refb,(750,1000))
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0 )
cv2.imshow(win_name, out_refb)
cv2.resizeWindow(win_name, 750, 1000)
cv2.imshow("Blue Channel Matched", out_refb)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)


win_name = 'Blue Channel Well Exposedness'
img = cv2.rotate(b, cv2.ROTATE_90_CLOCKWISE)
img = cv2.resize(b,(750,1000))
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0 )
cv2.imshow(win_name, b)
cv2.resizeWindow(win_name, 750, 1000)
cv2.imshow("Blue Channel Matched", b)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)


   
   
# img = opencvImage  # get image
# img_ref = cv2.imread("SendImage.png")  # get reference image

# denoised_img = non_local_means_filter(img)  # step 1. non local means filtering
# matched_img = histogram_matching(denoised_img, img_ref)  # step 2.1 histogram matching. Match input image with reference image
# (B, G, R) = cv2.split(matched_img)  # 2.2 get each channel of the matched image and find the following 9 channel
# outb_refb = match_histograms(image=B, reference=B, multichannel=False)  # Blue matched with blue
# outg_refb = match_histograms(image=G, reference=B, multichannel=False)  # Green matched with blue
# outr_refb = match_histograms(image=R, reference=B, multichannel=False)  # Red matched with blue

# outb_refg = match_histograms(image=B, reference=G, multichannel=False)  # Blue matched with green
# outg_refg = match_histograms(image=G, reference=G, multichannel=False)  # Green matched with green
# outr_refg = match_histograms(image=R, reference=G, multichannel=False)  # Red matched with green

# outb_refr = match_histograms(image=B, reference=R, multichannel=False)  # Blue matched with red
# outg_refr = match_histograms(image=G, reference=R, multichannel=False)  # Green matched with red
# outr_refr = match_histograms(image=R, reference=R, multichannel=False)  # Red matched with red

# pca = PCA()  # step 3.1 get PCA maps
# pca.fit(outb_refb)
# coeff = np.transpose(pca.components_)

# # step 3.2 get WE maps
# # step 3.3 get Saturation maps
# # step 4 laplacian filtering
# # step 5 calculating new channels and merging them

# #out_refb = cv2.merge([outb_refb, outg_refb, outr_refb])  # merge matched channels and get final b channel

# win_name = 'Original Image'
# cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
# cv2.moveWindow(win_name, 0, 0 )
# cv2.imshow(win_name, img)
# cv2.resizeWindow(win_name, 750, 1000)
# cv2.imshow("Original", img)
# cv2.waitKey(0); cv2.destroyAllWindows()
# cv2.waitKey(1)
# win_name = 'NLM Filtered'
# img = cv2.rotate(denoised_img, cv2.ROTATE_90_CLOCKWISE)
# img = cv2.resize(denoised_img,(750,1000))
# cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
# cv2.moveWindow(win_name, 0, 0 )
# cv2.imshow(win_name, denoised_img)
# cv2.resizeWindow(win_name, 750, 1000)
# cv2.imshow("NLM Filtered", denoised_img)
# cv2.waitKey(0); cv2.destroyAllWindows()
# cv2.waitKey(1)
# win_name = 'HM'
# img = cv2.rotate(matched_img, cv2.ROTATE_90_CLOCKWISE)
# img = cv2.resize(matched_img,(750,1000))
# cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
# cv2.moveWindow(win_name, 0, 0 )
# cv2.imshow(win_name, matched_img)
# cv2.resizeWindow(win_name, 750, 1000)
# cv2.imshow("HM", matched_img)
# cv2.waitKey(0); cv2.destroyAllWindows()
# cv2.waitKey(1)

