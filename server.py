import socket
from _thread import *
from log import *
from clock import Clock
from threading import Thread
import os
from dict_convert import *
import numpy as np
import pickle

client_sockets = []

ROUND_LIMIT = 100
round = 0

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

clock = Clock()
log = Log("Server.txt")


def client_index(client_socket):
    return client_sockets.index(client_socket) + 1


matrixList2d = []


def threaded(client_socket, addr):
    index = client_index(client_socket)
    name = f"Client{index}"
    dic = {"index": index}
    client_socket.sendall(pickle.dumps(dic))

    while True:
        if len(client_sockets) < 4:
            continue
        try:
            data = client_socket.recv(1024)
            if not data:
                log.write(
                    TimePrint(
                        f"Disconnected by {addr[0]} ({name})",
                        clock.get(),
                    )
                )
                break

            data = pickle.loads(data)

            if index % 2 == 0:
                dest = index - 1
            else:
                dest = index + 1

            if "arr" in data:
                TimePrint(f"Client{index}에서 Client{dest}로 {data} 전송")
                data["from"] = index
                client_sockets[dest - 1].sendall(pickle.dumps(data))

            log.write(
                TimePrint(
                    f"Received from {addr[0]} ({name}) >> {data}",
                    clock.get(),
                )
            )

        except ConnectionResetError as e:
            log.write(
                TimePrint(
                    f"Disconnected by {addr[0]} ({name})",
                    clock.get(),
                )
            )
            client_socket.close()
            break
        except ConnectionAbortedError as e:
            break


def server():
    global log
    log.write(TimePrint(f"Server start at {HOST}:{PORT}", clock.get()))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    log.write(TimePrint("Wait join client", clock.get()))
    print()
    log.write()
    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)
            start_new_thread(threaded, (client_socket, addr))
            TimePrint(f"Join {addr[0]} (Client{client_sockets.index(client_socket)+1})")

    except Exception as e:
        log.write(TimePrint(f"Error: {e}", clock.get()))


def close():
    for client in client_sockets:
        client.close()
    log.write(TimePrint("Server stopping...", clock.get()))
    log.save()
    os._exit(0)


server()
close()
