from operator import le
import socket
import struct
from PIL import Image
import io
import base64


HOST = "192.168.1.13"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)



print('SERVER STARTED RUNNING')
byte_array = bytearray()

while True:
    
    client, address = s.accept()


    data = client.recv(9999999)

    # data = data.decode('UTF-8')
    # print(data)

    a = base64.b64decode(data)
    
    print(a)

    # buff =  bytes([data, "utf-8"]);

    # size = struct.unpack("<h", buff)[0]
    # with open('image.jpg', 'wb') as f:
    #     while size > 0:
    #         data = client.recv(1024)
    #         f.write(data)
    #         size -= len(data)



    
    # data = bytearray(data)
    # listTestByte = list(data)

    # print(listTestByte)
 
    # image = Image.open(io.BytesIO(data))
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