
from os.path import exists as file_exists
import socket
import threading
import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.parser import RequestParser

# IP = socket.gethostbyname(socket.gethostname())

# default port number
PORT = 80
# ADDR = (IP,PORT)
MSG_SIZE = 1024
FORMAT = "utf-8"
POST_REQUEST = "POST"
GET_REQUEST = "GET"

OK_RESPONSE = "HTTP/1.1 200 OK\r\n"
NOT_FOUND_RESPONSE = "HTTP/1.1 404 Not Found\r\n"


class Server:
    def __init__(self, port_number=PORT):
        # inititing server  socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # IP = socket.gethostbyname(socket.gethostname())
        IP = "127.0.0.1"
        ADDR = (IP, port_number)
        # self.server.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 10000, 3000))

        self.server.bind(ADDR)

        self.server.listen()
        print("DEBUG : server is listening on IP:", IP, "PORT:", PORT)

    def start_server(self):

        while True:
            # waiting for client to connect
            conn, addr = self.server.accept()

            # creating new thread for each client
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))

            # starting thread  : will call handle_client() function
            thread.start()

            # show number of active threads (connections)
            # print("DEBUG : Number of active connections (threads)",(threading.active_count()-1))

    def handle_client(self, conn, addr):
        '''
        this function handles all client requests
        and creates a new thread for each client request (pipeline)
        the connection is closed after certain time delay (timeout)
        '''

        print("DEBUG : Client connected from:", addr)

        # setting timeout for client connection
        TIME_OUT_SEC = 15
        conn.settimeout(TIME_OUT_SEC)
        while True:
            try:
                # receiving client request
                msg = conn.recv(MSG_SIZE).decode(FORMAT)

                print(addr, ">", msg)

                # check if the received message is not empty
                # empty message means that client closed the connection
                if msg != "":
                    # parsing client request
                    client_request = RequestParser(msg)
                    # creating new thread to handle client request
                    thread = threading.Thread(
                        target=self.handle_client_request, args=(conn, addr, client_request))
                    thread.start()

                else:
                    # empty message means that client closed the connection
                    print(
                        "DEBUG EMPTY MESSAGE RECEIVED: Client disconnected from:", addr)
                    conn.close()
                    return

            except socket.timeout:
                # timeout means that client did not send any message
                print("DEBUG TIMEOUT : Server closes connection with :", addr)
                # close the connection with client
                conn.close()
                return
            except Exception as e:
                print("DEBUG ERROR : Server closes connection with :", addr)
                conn.close()
                return

    def handle_client_request(self, conn, addr, client_request):
        ''''
        this function called by handle_client() 
        and is called for each client request for the same connection

        '''
        try:

            if client_request.method == POST_REQUEST:
                self.handle_post_request(conn, addr, client_request)

            elif client_request.method == GET_REQUEST:
                self.handle_get_request(conn, addr, client_request)

        except socket.timeout:
            # timeout means that client did not send any message

            print("DEBUG TIMEOUT : Server closes connection with :", addr)
            # m = "HTTP/1.1 408 Request Timeout\r\n\r\n"
            # conn.send(m.encode(FORMAT))
            # close the connection with client
            conn.close()
            return
        except Exception as e:
            print("DEBUG ERROR : Server closes connection with :", addr)
            conn.close()
            return

    def handle_post_request(self, conn, addr, client_request):
        '''
        this function handles POST request
        '''

        msg = OK_RESPONSE+"\r\n"
        conn.send(msg.encode(FORMAT))

        filename = client_request.file_name
        # check if the file name is a directory or not

        if os.path.isdir(filename):
            # if directory then creates new directory
            os.makedirs(os.path.dirname(filename), exist_ok=True)

        # creates new file in the specified directory
        with open(filename, "w") as f:
            # write all received data from the client to the file
            f.write(client_request.data)

        print()
        print(addr, "> ", client_request.data)

    def handle_get_request(self, conn, addr, client_request):
        '''
        this function handles GET request
        '''

        # check if the file not exists
        if not file_exists(client_request.file_name):
            # if file not exists then send 404 error
            print("DEBUG: file not found")
            msg = NOT_FOUND_RESPONSE + "\r\n"
            conn.send(msg.encode(FORMAT))

            return
        else:
            # if file exists then send 200 OK and file content
            
            msg = OK_RESPONSE+"\r\n"
           
            file = open(client_request.file_name, "r")
            
        
            data = file.read()
            
            
            msg = msg+data+"\r\n"

            conn.send(msg.encode(FORMAT))
        

            file.close()

        return


if __name__ == "__main__":
    print("DEBUG : SERVER STARTED")
    server = Server()
    server.start_server()
    print("SERVER STOPPED")
