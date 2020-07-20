'''
基于select的IO多路复用并发模型
重点代码 !
'''

from socket import *
from select import select

HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)
sock = socket()
sock.bind(ADDR)
sock.listen(5)
#设置为非阻塞
sock.setblocking(False)

# IO对象监控列表
rlist = [sock]
wlist = []
xlist = []
#循环监听
while True:
    print(rlist)
    #对关注的IO对象进行监控
    rs,ws,xs = select(rlist,wlist,xlist)
    for r in rs:
        print(r.fileno())
        if r is sock:
            #处理客户端连接
            connfd, addr = rs[0].accept()
            print('connect from:', addr)
            connfd.setblocking(False)#设置为非阻塞
            rlist.append(connfd)  #添加到监控列表
        else:
            #收消息
            data = r.recv(1024)
            if not data:
                rlist.remove(r)
                r.close()
                continue
            print(data.decode())
            wlist.append(r)
    for w in ws:
        w.send(b'OK')
        wlist.remove(w)
