
from re import T
import socket
from threading import Thread
from os.path import exists
import sys

while True:
    msg =[]
    msg.append(input("cmd: "))
    msg.append(input("expos: "))
    msg.append(input("exfun: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 9999))
    sock.send(msg.encode())   
    msg = sock.recv(1024)
    print(msg.decode())
