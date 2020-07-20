from socket import *

sockfd = socket()
sockfd.connect(('0.0.0.0',8888))
while True:
    data = input("wo:")
    sockfd.send(data.encode())