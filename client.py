import socket
from _thread import *
from log import *
import sys
import random
import time

HOST = "127.0.0.1"
PORT = 9999

if len(sys.argv) == 2:
    HOST = sys.argv[1]

arg = sys.argv
if len(arg) == 2:
    HOST = arg[1]
elif len(arg) == 3:
    HOST = arg[1]
    PORT = arg[2]


printList = []

p = TimePrint(f"Try connection to {HOST}:{PORT}")
printList.append(p)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

p = TimePrint(f"Connected server to {HOST}")
p = ""
printList.append(p)

name: str
log: Log


def recv_data(client_socket):
    global log
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            client_socket.send("asd".encode())
        except Exception as e:
            client_socket.close()
            break


recv_data(client_socket)
log.write(TimePrint(f"Server stopped"))
log.save()
exit()
