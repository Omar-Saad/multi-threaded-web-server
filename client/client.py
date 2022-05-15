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
    def __init__(self, command):
        # creating HTTP request from the received command
        self.request, port_number = self.__createHTTPRequestFromCommand(
            command)
        # parsing HTTP request
        self.client_request = RequestParser(self.request)

        # inititing Server IP and port
        self.SERVER_IP = socket.gethostbyname(self.client_request.host_name)
        self.SERVER_PORT = port_number
        self.ADDR = (self.SERVER_IP, self.SERVER_PORT)

        self.client = None
        try:
            # connecting with the server
            self.client = self.__connect()
        except Exception as e:
            print("ERROR : WRONG HOST NAME OR PORT NUMBER")

    def sendHTTPRequest(self):
        '''
        this fuction sends an HTTP request 
        GET and POST
        '''
        if self.client == None:
            print("ERROR : COULD NOT CONNECT TO SERVER")
            return

        if self.client_request.method == "POST":

            request_to_send = self.request

            # read file data
            if file_exists(self.client_request.file_name):
                file = open(self.client_request.file_name, "r")
                data = file.read()

                request_to_send += data

                file.close()
            else:
                print("ERROR IN Client > File not found in client directory")
                self.client.close()
                return

            # upload file data to server
            self.client.send(request_to_send.encode(FORMAT))

            received_msg = self.client.recv(MSG_SIZE).decode(FORMAT)
            print("SERVER>")
            print(received_msg)

            self.client.close()

        elif self.client_request.method == "GET":
            self.client.send(self.request.encode(FORMAT))

            received_msg = self.client.recv(MSG_SIZE).decode(FORMAT)
            print("SERVER>")
            print(received_msg)

            response_parser = ResponseParser(received_msg)

            if response_parser.status == 200 and response_parser.data != None:
                #  download file in client directory
                file_name = self.client_request.file_name.split("/")[-1]
                file = open(file_name, "w")
                file.write(response_parser.data)
                file.close()

            self.client.close()

    def __connect(self):
        # initiating socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(self.ADDR)
        print("client is connected to IP:",
              self.SERVER_IP, "PORT:", self.SERVER_PORT)
        return client

    def __createHTTPRequestFromCommand(self, command, httpVersion=1.1):
        '''
        this function creates simple HTTP request from command
        '''
        request_lines = command.split(" ")
        method = request_lines[0]
        file_name = request_lines[1]
        host_name = request_lines[2]
        if len(request_lines) > 3:
            port_number = int(request_lines[3])
        else:
            port_number = 80
        request = method+" "+file_name + " HTTP/" + \
            str(httpVersion)+"\r\nHost:"+host_name + \
            ":"+str(port_number)+"\r\n\r\n"
        return request, port_number


# START OF CLIENT
if __name__ == "__main__":

    commands = []
    # check if input file name is given as argument
    if len(sys.argv) == 2:
        # read all commands from the input file
        file_name = sys.argv[1]
        file = open(file_name, "r")
        data = file.read()
        # list of commands in input file
        commands = data.split("\n")
        file.close()

    else:
        # take command from input terminal
        command = input(">")
        commands.append(command)

    print("CLIENT STARTED")

    # loop over commands
    for command in commands:
        # create a client request for each command
        client = Client(command.strip())
        client.sendHTTPRequest()
        print("\n")
        print("-------END OF COMMAND-------")
        print("\n")

    print("CLIENT CLOSED")
