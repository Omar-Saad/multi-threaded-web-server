class RequestParser:
    def __init__(self,request): 
        # parsing string
        request = request.strip()

        request_lines = request.split("\r\n")

        request_line_1 = request_lines[0].split(" ")
        self.method = request_line_1[0]
        self.file_name = request_line_1[1].replace("/","")
        if self.file_name == "":
            self.file_name = "index.html"

        
        self.httpVersion = request_line_1[2].split("/")[1]

        self.host_name = request_lines[1].split("Host:")[1].strip()
        self.header = request_lines[2:]
    
        
    def createHTTPRequest(self,httpVersion= 1.0):
        request = self.method+" / HTTP/"+str(httpVersion)+"\r\nHost:"+self.host_name+"\r\n\r\n"
        return request



class ResponseParser:
    def __init__(self,response): 
        # parsing string
        request_lines = response.split("\r\n")

        request_split = request_lines[0].split(" ")
        self.version = request_split[0]
        self.status = int(request_split[1])
        self.status_msg = request_split[2]
        self.header = "".join(request_lines[1:-1])

        self.data = None
        if self.status == 200:
            self.data = "".join(request_lines[-1:])
        
        