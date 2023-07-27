import os
import socket
from sys import exit

BUFFER = 1024
PORT = 3000
UDP_PORT = 6000
FORMAT = 'utf-8'
SERVER = '127.0.0.1'

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect((SERVER, PORT))

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client.bind((SERVER, UDP_PORT))

def downloadFile():
    data,addr = udp_client.recvfrom(1024)
    file = open(data.strip(),'wb')

    data,addr = udp_client.recvfrom(1024)
    try:
        while(data):
            file.write(data)
            udp_client.settimeout(1)
            data,addr = udp_client.recvfrom(1024)
    except:
        file.close()
        name = file.name.decode("utf-8")
        print (f"Downloaded {name}")

def downloadAllFiles():
    listDirSt = data_Server()
    with tcp_client,tcp_client.makefile('rb') as file:
        flag = True
        while flag:
            folder = file.readline()
            if not folder:
                break
            folder = folder.strip().decode()
            no_files = int(file.readline())
            path = os.path.join(os.curdir,folder.split('/')[-2])
            os.makedirs(path,exist_ok=True)
            list = []
            for i in range(no_files):
                filename = file.readline().strip().decode()
                filesize = int(file.readline())
                data = file.read(filesize)
                with open(os.path.join(path,filename),'wb') as f:
                    f.write(data)
                list.append(filename)
            f.close()
            print(f"Download {list}")
            flag = False
                         

def data_Server():
    okay = tcp_client.recv(1024).decode()
    print(okay)
    return okay


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (BUFFER - len(send_length))
    tcp_client.send(send_length)
    tcp_client.send(message)

    if msg == "listallfiles":
        data_Server()
    elif msg == "download all":
        downloadAllFiles() 
    elif msg == "exit":
        pass
    else:
        downloadFile()

while True:
    msg = input('> ')
    if msg != 'exit':
        send(msg)
    else:
        print('exiting')
        exit()