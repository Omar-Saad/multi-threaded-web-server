from http import client
import socket
import sys
import os.path
from os.path import exists as file_exists

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
 
from utils.parser import *


# constants
MSG_SIZE = 1024
FORMAT = "utf-8"

class Client:
    def __init__(self,command):
        self.request,port_number = self.__createHTTPRequestFromCommand(command)
        self.client_request = RequestParser(self.request)

        self.SERVER_IP = socket.gethostbyname(self.client_request.host_name)
        self.SERVER_PORT = port_number
        self.ADDR = (self.SERVER_IP,self.SERVER_PORT)

        self.client = self.__connect()


    def sendHTTPRequest(self):


        if self.client_request.method == "POST" and response_parser.status == 200:
            # self.client.send(self.request.encode(FORMAT))

            # received_msg = self.client.recv(MSG_SIZE).decode(FORMAT)
            # print("SERVER>")
            # print(received_msg)
            request_to_send = self.request
            
            # read file data
            if file_exists(self.client_request.file_name):
                file = open(self.client_request.file_name,"r")
                data = file.read()

                request_to_send += data

                file.close()
            else:
                print("ERROR IN Client > File not found in client directory")
                

            # upload file data to server
            self.client.send(request_to_send.encode(FORMAT))

            received_msg = self.client.recv(MSG_SIZE).decode(FORMAT)
            print("SERVER>")
            print(received_msg)

            self.client.close()
        
        elif self.client_request.method == "GET" :
            self.client.send(self.request.encode(FORMAT))

            received_msg = self.client.recv(MSG_SIZE).decode(FORMAT)
            print("SERVER>")
            print(received_msg)

            response_parser = ResponseParser(received_msg)

            if response_parser.status == 200 and response_parser.data!=None:
            #  download file in client directory
                file = open(self.client_request.file_name,"w")
                file.write(response_parser.data)
                file.close()

            self.client.close()

    
    def __connect(self):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        client.connect(self.ADDR)
        print("client is connected to IP:",self.SERVER_IP,"PORT:",self.SERVER_PORT)
        return client

    def __createHTTPRequestFromCommand(self,command,httpVersion= 1.1):
        request_lines = command.split(" ")
        method = request_lines[0]
        file_name = request_lines[1]
        host_name = request_lines[2]
        if len(request_lines) > 3:
            port_number = int(request_lines[3])
        else:
            port_number = 80
        request = method+" "+file_name +" HTTP/"+str(httpVersion)+"\r\nHost:"+host_name+"\r\n\r\n"
        return request,port_number



# START OF CLIENT
if __name__=="__main__":
    
    print("CLIENT STARTED")

    command = input(">")

    client = Client(command)
    client.sendHTTPRequest()

    print("CLIENT CLOSED")


    
