import requests
import socket

#r = requests.get('0.0.0.0:8000/README.me')

s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
s.connect(('0.0.0.0', 8000))
s.send('README.me'.encode('utf-8'))
response = s.recv(1024)

print(str(response))
