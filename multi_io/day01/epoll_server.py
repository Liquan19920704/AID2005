'''
基于epoll的IO多路复用并发模型
重点代码 !
'''

from socket import *
from select import *

HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)
sock = socket()
sock.bind(ADDR)
sock.listen(5)
#设置为非阻塞
sock.setblocking(False)
p=epoll()
p.register(sock,POLLIN)
map = {sock.fileno():sock,}
#循环监听
while True:
    #对关注的IO对象进行监控
    events = p.poll()
    #events--->[(fileno,event),()...]
    for r in events:
        #分情况讨论
        if r[0] == sock.fileno():
            #处理客户端连接
            connfd, addr = map[r[0]].accept()
            print('connect from:', addr)
            connfd.setblocking(False)#设置为非阻塞
            p.register(connfd,EPOLLIN|EPOLLERR)  #添加到监控
            map[connfd.fileno()]=connfd#同时维护字典
        elif r[1]==EPOLLIN:
            #收消息
            data = map[r[0]].recv(1024)
            if not data:
                p.unregister(map[r[0]])#p.unregister(fd) 参数可以使用事件对象,也可以是文件描述符
                map[r[0]].close()
                del map[r[0]]       #从字典移除
                continue
            print(data.decode())
            map[r[0]].send(b'OK')
        # for w in ws:
        #     w.send(b'OK')
        #     wlist.remove(w)
