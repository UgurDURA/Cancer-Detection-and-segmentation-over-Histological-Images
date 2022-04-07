#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 08:39:23 2022

@author: ugur_dura
"""

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
sock.bind(("192.168.1.8", 12345))

while True:
    data,addr = sock.recvfrom(5555)
    print(str(data))
    message = bytes("Hello Android ").encode("utf-8")
    sock.sendto(message, addr)