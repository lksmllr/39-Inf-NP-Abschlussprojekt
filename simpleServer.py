import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("localhost", 8000)
server.bind(server_address)

server.listen(5)

read = server.recv(1024)
print("Received: "+read.decode('utf-8'))
