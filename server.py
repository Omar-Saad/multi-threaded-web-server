import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (IP,PORT)
MSG_SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
# IP = "127.0.0.1"


def handle_client(conn,addr):
    print("Client connected from:",addr)
    connected = True
    while connected:
        msg = conn.recv(MSG_SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
        
        print(addr,">",msg)
        msg = "HTTP/1.1 404 NOT FOUND.\r\n"
        conn.send(msg.encode(FORMAT))
    conn.close()

if __name__=="__main__":
    print("SERVER STARTED")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("server is listening on IP:",IP,"PORT:",PORT)

    while True:
        conn,addr = server.accept()
        # print("Client connected from:",addr)
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        # show number of active threads (connections)
        print("Number of active connections (threads)",(threading.active_count()-1))

        
