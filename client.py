import socket
from _thread import *
from log import *
import sys
import random
import time
from dict_convert import *
from matrix import *
from threading import Thread
import pickle

HOST = "192.168.219.117"
PORT = 9999

if len(sys.argv) == 2:
    HOST = sys.argv[1]

arg = sys.argv
if len(arg) == 2:
    HOST = arg[1]
elif len(arg) == 3:
    HOST = arg[1]
    PORT = int(arg[2])


printList = []

p = TimePrint(f"Try connection to {HOST}:{PORT}")
printList.append(p)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 연결 수립
client_socket.connect((HOST, PORT))

p = TimePrint(f"Connected server to {HOST}")
p = ""
printList.append(p)

index: int
name: str
log: Log

# 클라이언트 이름 지정, 로그 생성
while True:
    data = client_socket.recv(1024)
    if not data:
        print("not data")
        break
    data = pickle.loads(data)
    if "index" in data:
        index = data["index"]
        name = f"Client{index}"
        log = Log(name + ".txt")
        for p in printList:
            log.write(p)
        break


def send_round(data):
    """
    행 또는 열을 순차적으로 보냄
    """

    matrix = random_matrix()
    for i in range(10):
        if index % 2 == 0:
            arr = extract_row(matrix, i)
        else:
            arr = extract_col(matrix, i)
        dic = {"arr": arr_to_str(arr)}

        TimePrint(f"Client{index} >> {dic} 전송")
        client_socket.send(pickle.dumps(dic))

        # Done 응답을 받을 때 까지 기다림
        while True:
            data = client_socket.recv(1024)
            if not data:
                continue
            data = pickle.loads(data)
            if "Done" in data:
                break
            pass


def send_element(arr):
    for element in arr:
        print(element, end=" ")
        if index == 1:
            dest = 2
        elif index == 2:
            dest = 3
        elif index == 3:
            dest = 0
        elif index == 4:
            dest = 1
        dic = {"element": element, "dest": dest}
        client_socket.sendall(pickle.dumps(dic))
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("not data")
                break
            data = pickle.loads(data)
            if "element" in data and "done" in data:
                break
    print()


def recv_round(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            print("not data")
            break

        data = pickle.loads(data)
        if "arr" in data:
            print(f"received from  {data['from']}>> ", end="")

            # 다른 스래드에서 배열의 요소를 보냄
            send_element_thread = Thread(target=send_element, args=data["arr"])
            send_element_thread.daemon = True
            send_element_thread.start()


start_new_thread(send_round, (client_socket,))
# start_new_thread(recv_round, (client_socket,))
recv_round(client_socket)
# log.write(TimePrint(f"Server stopped"))
# log.save()
# exit()
