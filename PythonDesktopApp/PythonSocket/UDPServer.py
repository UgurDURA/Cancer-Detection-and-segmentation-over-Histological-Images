from email.mime import base
from lib2to3.pgen2.token import VBAR
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

# from cbcr import cbcr_transform
# from well_exposedness import well_exposedness

# ImageFile.LOAD_TRUNCATED_IMAGES = True
# import matplotlib.pyplot as plt
# import pca_last

# from skimage.restoration import denoise_nl_means, estimate_sigma
# from skimage.exposure import match_histograms
# from sklearn.decomposition import PCA
# import non_local_means_filter
# import histogram_matching
# import math


from tkinter import *
from PIL import ImageTk, Image


HOST = "192.168.1.6"
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
    opencvImage = cv2.resize(opencvImage,(1920,1080))


    root = Tk()
    root.title("MicrosPhone")    
    # imgReceived = imgReceived.rotate(90)
    imgReceived = imgReceived.resize((540,960))
    my_image = ImageTk.PhotoImage(imgReceived)
    my_label = Label(image=my_image)
    my_label.grid(row=1, column=1, columnspan=3)

    b_capture = Button(root, text = "Capture")
    b_exit = Button(root, text= "Exit", command=root.quit)
    b_zoom_in = Button(root, text="+")
    b_zoom_out = Button(root, text="-")


    b_capture.grid(row=1,column=0)
    b_zoom_in.grid(row=2,column=0)
    b_zoom_out.grid(row=3,column=0)
    b_exit.grid(row=4,column=0)
    root.mainloop()

  
    
    

    

client.close()
s.close()

############################################################################################################################################

                                                                            #Receive the input
                                                                            
############################################################################################################################################

img = opencvImage
img_ref = cv2.imread("Kidney_000_Mıcroscope_4x_1.09_HuwDevıce.png")

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

WBB = cv2.Laplacian((PBB * EBB * DBB), cv2.CV_64F)
WGB = cv2.Laplacian((PGB * EGB * DBB), cv2.CV_64F)
WRB = cv2.Laplacian((PRB * ERB * DRB), cv2.CV_64F)

WBG = cv2.Laplacian((PBG * EBG * DBG), cv2.CV_64F)
WGG = cv2.Laplacian((PGG * EGG * DGG), cv2.CV_64F)
WRG = cv2.Laplacian((PRG * ERG * DRG), cv2.CV_64F)

WBR = cv2.Laplacian((PBR * EBR * DBR), cv2.CV_64F)
WGR = cv2.Laplacian((PGR * EGR * DGR), cv2.CV_64F)
WRR = cv2.Laplacian((PRR * ERR * DRR), cv2.CV_64F)

############################################################################################################################################

                                                                #Reconstructing the Color Channels

############################################################################################################################################

recons_B = ((RB * WRB) + (GB * WGB) + (BB * WBB)) / (WRB + WGB + WBB)
recons_G = ((RG * WRG) + (GG * WGG) + (BG * WBG)) / (WRG + WGG + WBG)
recons_R = ((RR * WRR) + (GR * WGR) + (BR * WBR)) / (WRR + WGR + WBR)

final_image = cv2.merge([recons_B, recons_G, recons_R])

Y, Cb, Cr = cbcr_transform(final_image)
refY, refCb, refCr = cbcr_transform(img_ref)

matched_Cb = match_histograms(image=Cb, reference=refCb, multichannel=False)
matched_Cr = match_histograms(image=Cr, reference=refCr, multichannel=False)

Y = np.asarray(Y, dtype=np.uint8)
matched_Cb = np.asarray(matched_Cb, dtype=np.uint8)
matched_Cr = np.asarray(matched_Cr, dtype=np.uint8)

final_YCbCr = cv2.merge([Y, matched_Cb, matched_Cr])
final_BGR = cv2.cvtColor(final_YCbCr, cv2.COLOR_YCrCb2BGR)

############################################################################################################################################

                                                                #Display Each Result

############################################################################################################################################



win_name = 'Original Image'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0)
cv2.imshow(win_name, img)
cv2.resizeWindow(win_name, 1920,1080)
cv2.imshow("Original", img)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)



win_name = 'Final YBCR'
img = cv2.rotate(final_YCbCr, cv2.ROTATE_90_CLOCKWISE)
img = cv2.resize(final_YCbCr,(1920,1080))
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0 )
cv2.imshow(win_name, final_YCbCr)
cv2.resizeWindow(win_name, 1920,1080)
cv2.imshow("Final YBCR", final_YCbCr)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)

win_name = 'FINAL BGR'
img = cv2.rotate(final_BGR , cv2.ROTATE_90_CLOCKWISE)
img = cv2.resize(final_BGR ,(750,1000))
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0 )
cv2.imshow(win_name, final_BGR )
cv2.resizeWindow(win_name, 1920,1080)
cv2.imshow("FINAL RGB", final_BGR )
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

