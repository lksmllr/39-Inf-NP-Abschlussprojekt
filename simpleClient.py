#!/usr/bin/env python3

import socket
import sys
import argparse

# parse arguments
parser = argparse.ArgumentParser(description="FastaGenScript")
parser.add_argument("host", type=str, help="HostName")
parser.add_argument("port", type=str, help="Port")
parser.add_argument("command", type=str, help="Command")
args = parser.parse_args()

# establish connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
sockaddr = (args.host, int(args.port));
s.connect(sockaddr)

messageAsLines = args.command.split()
i = 0
closed = False
while ( (not s.timeout) or (not closed) ):
    # send bytes to server
    if (i < len(messageAsLines)):
        print("Sending now line "+str(i)+" to Server: "+messageAsLines[i])
        sentbytes = s.send(messageAsLines[i].encode('utf-8'))
    # read bytes from server
    if (i < len(messageAsLines)):
        print("Waiting for Server to receive line")
        buffersize = len(messageAsLines[i].encode('utf-8'))
        recbytes = s.recv(buffersize)
        recbytes = recbytes.decode('utf-8')
        print("Response from "+args.host+", "+args.port+": "+recbytes)
    elif (len(messageAsLines) == i):
        closed = True
    i = i + 1

# close connection
s.close()
