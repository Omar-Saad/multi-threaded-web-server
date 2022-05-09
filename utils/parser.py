class RequestParser:
    def __init__(self,request): 
        # parsing string
        request_split = request.split(" ")
        self.method = request_split[0]
        self.file_name = request_split[1]
        self.host_name = request_split[2]
        if len(request_split) > 3:
            self.port_number = int(request_split[3])
        else:
            self.port_number = 80


class ResponseParser:
    def __init__(self,response): 
        # parsing string
        request_lines = response.split("\n")

        request_split = request_lines[0].split(" ")
        self.version = request_split[0]
        self.status = int(request_split[1])
        self.status_msg = request_split[2]
        self.data = None
        if len(request_lines) > 2:
            self.data = "".join(request_lines[1:])
        
