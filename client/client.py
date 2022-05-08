from http import client
import socket
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
 
from utils.client_request import ClientRequest

# SERVER_IP = socket.gethostbyname(socket.gethostname())
# SERVER_PORT = 5000
# ADDR = (SERVER_IP,SERVER_PORT)

# DISCONNECT_MSG = "!DISCONNECT"

# constants
MSG_SIZE = 1024
FORMAT = "utf-8"


def parse_request(request):
    request_split = request.split(" ")
    method = request_split[0]
    file_name = request_split[1]
    host_name = request_split[2]
    if len(request_split) > 3:
        port_number = request_split[3]
    else:
        port_number = 80
    
    return (method,file_name,host_name,str(port_number))

if __name__=="__main__":
    

    
    print("CLIENT STARTED")
    msg = input(">")
    client_request = ClientRequest(msg)
    SERVER_IP = socket.gethostbyname(client_request.host_name)

    SERVER_PORT = client_request.port_number
    ADDR = (SERVER_IP,SERVER_PORT)

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    

    client.connect(ADDR)
    print("client is connected to IP:",SERVER_IP,"PORT:",SERVER_PORT)
    client.send(msg.encode(FORMAT))
    msg = client.recv(MSG_SIZE).decode(FORMAT)
    print("SERVER>",msg)

    if client_request.method == "POST":

        file = open(client_request.file_name,"r")
        data = file.read()

        client.send(data.encode(FORMAT))
        file.close()
        client.close()
    
    # elif client_request.method == "GET":
    #      file = open(client_request.file_name,"w")

    #      file.write()



        
        
        # if msg == DISCONNECT_MSG:
        #     connected = False
        # else:
        #     msg = client.recv(MSG_SIZE).decode(FORMAT)
        #     print("SERVER>",msg)




    
