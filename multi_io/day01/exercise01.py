from socket import *
import time

f = open('./log','a+')
sockfd = socket()
sockfd.bind(('0.0.0.0',8888))
sockfd.listen(5)

# sockfd.settimeout(3)
sockfd.setblocking(False)
while True:
    print('waiting for connect')
    try:
        connfd,addr = sockfd.accept()
        print('connect from ',addr)
    except BlockingIOError as e :
        #干点别的事
        msg = "%s:%s\n"%(time.ctime(),e)
        f.write(msg)
        time.sleep(2)
    except timeout as e:
        msg = "%s:%s\n"%(time.ctime(),e)
        f.write(msg)
    else:
        data = connfd.recv(1024)
        print(data.decode())