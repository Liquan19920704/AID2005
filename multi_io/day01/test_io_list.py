from socket import *
from select import  select

udp_sockfd = socket(AF_INET,SOCK_DGRAM)
udp_sockfd.bind(('0.0.0.0',8888))

tcp_sockfd = socket()
tcp_sockfd.bind(('0.0.0.0',8899))
tcp_sockfd.listen(5)
connfd,addr = tcp_sockfd.accept()



f = open('./log','rb')
print('监听IO发生')
rs,ws,xs = select([connfd],[],[])
print(rs)
print(ws)
print(xs)
