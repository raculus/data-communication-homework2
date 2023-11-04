import socket
from _thread import *
from log import *
from clock import Clock
from threading import Thread
import os
from dict_convert import *

client_sockets = []

ROUND_LIMIT = 100
round = 0

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

clock = Clock()
log = Log("Server.txt")


def client_name(client_socket):
    return f"Client{client_sockets.index(client_socket)+1}"


def threaded(client_socket, addr):
    name = client_name(client_socket)
    dic = {"name": name}
    client_socket.send(dict_to_str(dic).encode())

    while True:
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
            log.write(
                TimePrint(
                    f"Received from {addr[0]} ({name}) >> {data.decode('utf-8')}",
                    clock.get(),
                )
            )

            receivedData = data.decode("utf-8")

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
            client_thread = Thread(target=threaded, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()

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
