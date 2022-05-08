class ClientRequest:
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
