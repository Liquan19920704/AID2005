from socket import *

s = socket()
s.bind(('0.0.0.0',8889))
s.listen()
c,addr=s.accept()
data = c.recv(1024)
print(data)
print(type(s))
print(type(c))
print(type(s) is type(c))