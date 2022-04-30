from http import client
import socket

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
ADDR = (SERVER_IP,SERVER_PORT)
MSG_SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


if __name__=="__main__":
    print("CLIENT STARTED")
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    print("client is connected to IP:",SERVER_IP,"PORT:",SERVER_PORT)

    connected = True
    while connected:
        msg = input(">")
        if msg == DISCONNECT_MSG:
            connected = False
        client.send(msg.encode(FORMAT))
        
        if msg == DISCONNECT_MSG:
            connected = False
        else:
            msg = client.recv(MSG_SIZE).decode(FORMAT)
            print("SERVER>",msg)
