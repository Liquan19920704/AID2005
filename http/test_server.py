from socket import *
s= socket()
s.bind(('0.0.0.0',8888))
s.listen(5)
while True:
    c,addr= s.accept()
    print('connect from ',addr)
    data = c.recv(4096)
    print(data.decode().split('\n')[0])
    f = open('/home/tarena/桌面/网络并发编程/info/static/index.html', 'rb')
    n = f.read(1024 * 1024)
    if data =='':
        c.close()
    html =f"""HTTP/1.1 200 OK
    Content0Type:text/html

    {n.decode()}
    """
    c.send(html.encode())

