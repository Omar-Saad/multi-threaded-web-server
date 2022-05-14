class RequestParser:
    def __init__(self,request): 
        # parsing string

        request = request.strip()

        request_split = request.split("\r\n\r\n")
        request_header = request_split[0]

        request_header_lines = request_header.split("\r\n")

        request_line_1 = request_header_lines[0].split(" ")
        self.method = request_line_1[0]

        request_line_1[1] = request_line_1[1].strip()
        
        if request_line_1[1][0] == "/":
            request_line_1[1] = request_line_1[1].replace("/","",1)
        
            
        self.file_name = request_line_1[1]

        if self.file_name == "":
            self.file_name = "index.html"

        
        self.httpVersion = request_line_1[2].split("/")[1]

        host_port_line = request_header_lines[1].split(":")
        self.host_name = host_port_line[1].strip()
        if len(host_port_line) > 2:
            self.port_number = int(host_port_line[2].strip())
        else:
            self.port_number = 80

        # self.host_name = request_header_lines[1].split("Host:")[1].strip()
        self.header = request_header

        self.data = None
        if len(request_split) > 1:
            self.data = request_split[1]
    


class ResponseParser:
    def __init__(self,response): 
        # parsing string
        response_split = response.split("\r\n\r\n")
        response_header = response_split[0]

        response_header_lines = response_header.split("\r\n")

        response_header_line_1 = response_header_lines[0].split(" ")
        self.version = response_header_line_1[0]
        self.status = int(response_header_line_1[1])
        self.status_msg = response_header_line_1[2]

        self.header = response_header

      

        self.data = None
        if len(response_split) >1 :
            self.data = response_split[1]
     
        