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
 


HOST = "192.168.1.144"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)



print('SERVER STARTED RUNNING')


while True:
    
    # client, address = s.accept()


    # data = client.recv(9999999)

    # print(data)

    # data = data.decode('UTF-8')
    # print(data)

    # imageBytes= base64.b64decode(data)
    # print(imageBytes)

    # decoded = cv2.imdecode(np.frombuffer(imageBytes, np.uint8), -1)

    # print(decoded)

    # cv2.imshow("Decoded image", decoded)

    


    

    # grayImage = np.array(a).reshape(4000, 3000 )

    # flatNumpyArray = np.array(a)
    # grayImage = flatNumpyArray.reshape(300, 400)
    # cv2.imshow("image",grayImage)

    

    # numpyarray = np.asarray(ba, dtype=np.uint16)
    # bgrImage = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)


    # print(decodedData)

    # image = np.fromstring(decodedData, np.uint8)
    # image = cv2.cvtColor(image, cv2.COLOR_BayerRG2RGB)
    # cv2.imshow(bgrImage)



    # buff =  bytes([data, "utf-8"]);

    # size = struct.unpack("<h", buff)[0]
    # with open('image.jpg', 'wb') as f:
    #     while size > 0:
    #         data = client.recv(1024)
    #         f.write(data)
    #         size -= len(data)


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

    # b= base64.b64decode(data)        
    # data = list(data)

    # print(data) 
    # decoded = cv2.imdecode(np.frombuffer(data, np.uint8), -1)
    # data_decoded = int.from_bytes(data, byteorder="big")
    # data_decoded = data_decoded.decode()
    # print(data_decoded)


    # numbers = np.array(imageBytes)
    # x = numbers[::2]
    # y = numbers[1::2]

    # plt.plot(x, y)
    # plt.show()  


    # decoded = cv2.imdecode(np.frombuffer(imageBytes, np.uint8), -1)
    # image = cv2.cvtColor(data, cv2.COLOR_BayerRG2RGB)
    # pi = Image.fromarray(cv2.cvtColor(imageBytes, cv2.COLOR_BGR2RGB)) 
     


    # print(decoded)

 
    # image = Image.open(io.BytesIO(imageBytes))
    # image.show()

    # buf = ''
    # while len(buf) < 4:
    #     buf += client.recv(4 - len(buf))
    # size = struct.unpack('!i', buf)[0]
    # with open('image.jpg', 'wb') as f:
    #     while size > 0:
    #         data = client.recv(1024)
    #         f.write(data)
    #         size -= len(data)

    print('Packet Received')

    # with open("my_file.dng", "wb") as binary_file:
    #     binary_file.write(data)

    # img = Image.fromstring('L', (3000,4000), data, 'raw', 'F;16')
    img= Image.open(io.BytesIO(data))
    # img= img.convert('RGB')
    # open_cv_image = np.array(img)
    # open_cv_image = open_cv_image[:, :, ::-1].copy() 

    img.show()

    # cv2.imshow("From Android Phone", open_cv_image)

    # cv2.imshow("Display window",np.array(data).reshape(3000,4000).astype(np.uint8))
    client.close()
s.close()   
 