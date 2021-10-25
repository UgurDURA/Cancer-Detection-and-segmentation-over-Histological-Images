#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 16:35:55 2021

@author: ugur_dura
"""

import socket, cv2, pickle, struct

#creating the socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "192.168.1.9"
port = 9999

client_socket.connect((host_ip, port)) # a tuple

data = b""
payload_size = struct.calcsize("Q")

while True:
    
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) #4k
        if not packet:break
        data +=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    
    while len(data) <msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    
    
    
    
    
    
    cv2.imshow("Received",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
        
          
        
client_socket.close()
            