from socket import *

sockfd=socket()
sockfd.connect(('127.0.0.1',8888))
while True:
    try:
        sockfd.send(input('wo').encode())
        data = sockfd.recv(1024)
        print(data.decode())
    except KeyboardInterrupt as e:
        sockfd.close()
        print('客户端退出')