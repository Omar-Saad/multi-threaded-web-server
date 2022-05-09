import socket
import threading
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from os.path import exists as file_exists
 
from utils.parser import RequestParser

IP = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (IP,PORT)
MSG_SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
POST_REQUEST = "POST"
GET_REQUEST = "GET"

OK_RESPONSE = "HTTP/1.0 200 OK.\r\n"
NOT_FOUND_RESPONSE = "HTTP/1.0 404 Not Found\r\n"
# IP = "127.0.0.1"



def handle_client(conn,addr):
    print("Client connected from:",addr)
    
    # while connected:
    msg = conn.recv(MSG_SIZE).decode(FORMAT)
    client_request = RequestParser(msg)
    
    print(addr,">",msg)
    if client_request.method == POST_REQUEST:
        handle_post_request(conn,addr,client_request)
        return

    elif client_request.method == GET_REQUEST:
         handle_get_request(conn,addr,client_request)
         return

        

    # msg = "HTTP/1.1 404 NOT FOUND.\r\n"
    # conn.send(msg.encode(FORMAT))


    # conn.close()
    # print("connection closed with ",addr)

def handle_post_request(conn,addr,client_request):

    conn.send(OK_RESPONSE.encode(FORMAT))
    file = open(client_request.file_name,"w")
    data = conn.recv(MSG_SIZE).decode(FORMAT)
    file.write(data)
    file.close()
    conn.close()
    print()
    print(addr,"> ",data)


def handle_get_request(conn,addr,client_request):

    if not file_exists(client_request.file_name):
        conn.send(NOT_FOUND_RESPONSE.encode(FORMAT))
        conn.close()
        return
    else:

        msg = OK_RESPONSE

        file = open(client_request.file_name,"r")
        data = file.read()
        msg = msg+data+"\r\n"
        
        conn.send(msg.encode(FORMAT))
        
        file.close()
        conn.close()
        


if __name__=="__main__":
    print("SERVER STARTED")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("server is listening on IP:",IP,"PORT:",PORT)

    while True:
        
        conn,addr = server.accept()
        
        
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        # show number of active threads (connections)
        print("Number of active connections (threads)",(threading.active_count()-1))

        


        
    # return (method,file_name,host_name,str(port_number))
        