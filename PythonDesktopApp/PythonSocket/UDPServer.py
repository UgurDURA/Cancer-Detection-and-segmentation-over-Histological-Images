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
 
    img= Image.open(io.BytesIO(data))
    # img = img.save("SendImage.png")
    # opencvImage = cv2.imread("SendImage.png")
    opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
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
s.close()   
 