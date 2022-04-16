from operator import le
import socket
import struct
from PIL import Image
import io
import base64
import numpy as np
import cv2 as cv2
import binascii
import struct
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import matplotlib.pyplot as plt


HOST = "192.168.1.13"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)



print('SERVER STARTED RUNNING')
byte_array = bytearray()

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


    data = client.recv(4096)
    print(data)

    print("data received")

    # print(data) 
    # decoded = cv2.imdecode(np.frombuffer(data, np.uint8), -1)

    
    data = bytearray(data)

    listTestByte = list(data)

    print(listTestByte)
    print(data)
    imageBytes= bytearray(base64.b64decode(data))
    # imageBytes = np.array(imageBytes)
    listTestByte2 = list(imageBytes)
    print(listTestByte2)
 

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
client.close()
s.close()   
 