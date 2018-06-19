#!/usr/bin/env python3

import socket
import sys
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.bind(('localhost', 2005))
s.listen(socket.SOMAXCONN)
try:
    inSocket, addr = s.accept()
    # lalala
    msg1 = "Hello "+str(addr[0])+":"+str(addr[1])+" nice to meet you!"
    msg2 = time.strftime('%X %x %Z')
    print(msg1)
    print(msg2)
finally:
    inSocket.close()
