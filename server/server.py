import socket
import threading
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from os.path import exists as file_exists
 
from utils.parser import RequestParser

# IP = socket.gethostbyname(socket.gethostname())
PORT = 80
# ADDR = (IP,PORT)
MSG_SIZE = 1024
FORMAT = "utf-8"
POST_REQUEST = "POST"
GET_REQUEST = "GET"

OK_RESPONSE = "HTTP/1.1 200 OK\r\n"
NOT_FOUND_RESPONSE = "HTTP/1.1 404 Not Found\r\n"


class Server:
    def __init__(self,port_number = PORT):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # IP = socket.gethostbyname(socket.gethostname())
        IP = "127.0.0.1"
        ADDR = (IP,port_number)

        self.server.bind(ADDR)
        self.server.listen()
        print("DEBUG : server is listening on IP:",IP,"PORT:",PORT)

    def start_server(self):
        while True:
        
            conn,addr = self.server.accept()
            
            thread = threading.Thread(target=self.handle_client,args=(conn,addr))
            thread.start()
            # show number of active threads (connections)
            print("DEBUG : Number of active connections (threads)",(threading.active_count()-1))
    

    

    def handle_client(self,conn,addr):
        print("DEBUG : Client connected from:",addr)
        
        msg = conn.recv(MSG_SIZE).decode(FORMAT)
        print(addr,">",msg)
        if msg != "":
            client_request = RequestParser(msg)
        else:
            conn.close()
            return
        
        if client_request.method == POST_REQUEST:
            self.handle_post_request(conn,addr,client_request)
            print("DEBUG : Client disconnected from:",addr)
            return

        elif client_request.method == GET_REQUEST:
            self.handle_get_request(conn,addr,client_request)
            print("DEBUG : Client disconnected from:",addr)
            return


    def handle_post_request(self,conn,addr,client_request):

        conn.send(OK_RESPONSE.encode(FORMAT))

        # data = conn.recv(MSG_SIZE).decode(FORMAT)

        filename = client_request.file_name
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(client_request.data)

        # file_name = client_request.file_name.split("/")[-1]
        # file = open(file_name,"w")
        
        # file.write(client_request.data)
        # file.close()

        conn.close()
        print()
        print(addr,"> ",client_request.data)
    
        
    def handle_get_request(self,conn,addr,client_request):
        
        if not file_exists(client_request.file_name):
            print("DEBUG: file not found")
            msg = NOT_FOUND_RESPONSE + "\r\n"
            conn.send(msg.encode(FORMAT))
            conn.close()
            return
        else:

            msg = OK_RESPONSE+"\r\n"
            print(client_request.file_name)
            file = open(client_request.file_name,"r")
            data = file.read()
            msg = msg+data+"\r\n"
    
            conn.send(msg.encode(FORMAT))
            
            file.close()
            conn.close()
  
            
       


if __name__=="__main__":
    print("DEBUG : SERVER STARTED")
    server = Server()
    server.start_server()
    print("SERVER STOPPED")