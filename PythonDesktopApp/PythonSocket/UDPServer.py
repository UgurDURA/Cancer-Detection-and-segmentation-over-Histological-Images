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
ImageFile.LOAD_TRUNCATED_IMAGES = True
import matplotlib.pyplot as plt

from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.exposure import match_histograms
from sklearn.decomposition import PCA
 


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
    # img = img.save("SendImage.png")
    # opencvImage = cv2.imread("SendImage.png")
    opencvImage = cv2.cvtColor(np.array(imgReceived), cv2.COLOR_RGB2BGR)
    
    opencvImage = cv2.rotate(opencvImage, cv2.ROTATE_90_CLOCKWISE)
    opencvImage = cv2.resize(opencvImage,(750,1000))
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

img = opencvImage
img_ref = cv2.imread("SendImage.png")

sigma_est = np.mean(estimate_sigma(img, multichannel=True))  # get sigma values from all the channels

denoise_img = cv2.fastNlMeansDenoisingColored(img, None, sigma_est, sigma_est, 5, 21)

matched = match_histograms(image=denoise_img, reference=img_ref, multichannel=True)

(B, G, R) = cv2.split(matched)

outb_refb = match_histograms(image=B, reference=B, multichannel=False)
outg_refb = match_histograms(image=G, reference=B, multichannel=False)
outr_refb = match_histograms(image=R, reference=B, multichannel=False)

out_refb = cv2.merge([outb_refb, outg_refb, outr_refb])
print(outb_refb.shape)
pca = PCA()
pca.fit(outb_refb)
coeff = np.transpose(pca.components_)

win_name = 'Original Image'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0 )
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

