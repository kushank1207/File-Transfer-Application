import os
import socket
import threading

PORT = 3000
UDP_PORT = 6000
SERVER = "localhost"
FORMAT = 'utf-8'

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((SERVER, PORT))

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Download a single file
def downloadFile(filename):
    if os.path.exists(filename):
        fname = filename.encode(FORMAT)
        udp_server.sendto(fname,(SERVER, UDP_PORT))
        f=open(filename,"rb")
        data = f.read(1024)
        while (data):
            if(udp_server.sendto(data,(SERVER, UDP_PORT))):
                data = f.read(1024)
        f.close()
    else:
        print("No such file exists.")

# List all the files
def listDirContents(conn):
    dirContent = os.listdir(os.curdir)
    print(dirContent)
    dirContentSt = ' '.join([str(x) for x in dirContent])
    conn.send(dirContentSt.encode(FORMAT))


# Download all the files in the server directory
def downloadAllFiles(conn):
    listDirContents(conn)
    folderlist = os.getcwd().split('/')
    folder = ''
    for i in range(len(folderlist)):
        folder += folderlist[i]+'/'
    print(folder)
    conn.sendall(folder.encode()+ b'\n')
    files = os.listdir(folder)
    conn.sendall(str(len(files)).encode() + b'\n')
    for file in files:
        path = os.path.join(folder,file)
        if os.path.isfile(path):
            filesize = os.path.getsize(path)
            conn.sendall(file.encode()+ b'\n')
            conn.sendall(str(filesize).encode() + b'\n')
            with open(path,'rb') as f:
                conn.sendall(f.read())




def client_handler(conn, addr):
    connected = True
    while connected:
        msg_length = conn.recv(1024).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == "exit":
                connected = False
                print("Disconnected")
                break

            elif msg == "listallfiles":
                listDirContents(conn)

            elif msg == "download all":
                downloadAllFiles(conn)

            else:
                fname = msg.split(' ')
                filename = fname[1]
                print(filename)
                downloadFile(filename)

def start():
    tcp_server.listen()
    print("server started")
    while True:
        conn, addr = tcp_server.accept()
        thread = threading.Thread(target = client_handler, args = (conn, addr))
        thread.start()
        print(f'Active Conn = {threading.active_count()-1}')

start()