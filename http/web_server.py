"""
web服务程序
假定:用户有一组网页,希望使用我们的类快速搭建一个服务,实现自己网页的展示浏览

IO多路复用 和http训练

3.设计原则
    *站在用户角度,想用法
            1.使用流程
            2.哪些量需要用户决定,怎么传入
                    哪组网页?     服务端地址?

    *能够为用户实现的,不麻烦使用者
    *不能替使用者决定的,提供接口(参数) 让用户方便传递或者
     让用户调用不同的方法做选择
"""
from socket import *
from select import select
import re,os
class WebServer:
    def __init__(self,host = '0.0.0.0',port = 8888,html = None):
        self.host = host
        self.port = port
        self.html = html
        #为IO多路复用并发模型做准备
        self.__rlist = []
        self.__wlist = []
        self.__xlist = []
        self.creatsock()
        self.bind()
    def creatsock(self):
        self.sock = socket()
        self.sock.setblocking(False)
    def bind(self):
        self.sock.bind((self.host,self.port))
    def start(self):
        self.sock.listen(5)
        print('Listen the port %s'%self.port)
        #IO多路复用并发模型
        self.__rlist.append(self.sock)
        while True:
            rs,ws,xs = select(self.__rlist,self.__wlist,self.__xlist)
            for i in rs:
                if i is self.sock:
                    #有浏览器连接
                    connfd,addr = self.sock.accept()
                    print('connect from ',addr)
                    connfd.setblocking(False)
                    self.__rlist.append(connfd)
                else:
                    #有客户端发送请求
                     try:
                        self.handle(i)
                     except:
                         self.__rlist.remove(i)
                         i.close()

    #处理客户端请求
    def handle(self, connfd):
        #浏览器发送了http请求
        try:
            request = connfd.recv(1024*10).decode()
        # print(request)
        #使用正则提取请求内容
            pattern = '[A-Z]+\s+(?P<info>/\S*)'
            result = re.match(pattern,request)  #match对象 None
        except:
            self.__rlist.remove(connfd)
            connfd.close()
        else:
            if result:
                info = result.group('info')#提取请求内容
                print('请求内容',info)
                self.send_response(connfd,info)
            else:
                #断开客户端
                self.__rlist.remove(connfd)
                connfd.close()

    def send_response(self, connfd, info):
        if info =='/':
            path = self.html+'/index.html'
        else:
            path = self.html+info
        print(path)
        if os.path.exists(path):
            file = open(path,'rb')
            data = file.read(1024*1024)
            print('打开文件')
            response = b"HTTP/1.1 200 OK\r\n"
            response+=b"Content-Type:text/html\r\n"
            response+=b"Content-Length:%d\r\n"%len(data)
            response+=b"\r\n"
            response+=data
            print('response:',response)
            connfd.send(response)
            print('已发送')
        else:
            print('报错')
            html = f"""HTTP/1.1 404 NotFound
            Content-Type:text/html

            404error
            """
            connfd.send(html.encode())

if __name__ == '__main__':
    https= WebServer(host= '0.0.0.0',port = 8888,html = '/home/tarena/static')#实例化对象
    https.start()