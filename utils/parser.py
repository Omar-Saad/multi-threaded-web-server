class RequestParser:
    def __init__(self,request): 
        # parsing string

        request = request.strip()

        request_split = request.split("\r\n\r\n")
        request_header = request_split[0]

        request_header_lines = request_header.split("\r\n")

        request_line_1 = request_header_lines[0].split(" ")
        self.method = request_line_1[0]
        self.file_name = request_line_1[1].replace("/","")
        if self.file_name == "":
            self.file_name = "index.html"

        
        self.httpVersion = request_line_1[2].split("/")[1]

        self.host_name = request_header_lines[1].split("Host:")[1].strip()
        self.header = request_header

        self.data = None
        if len(request_split) > 1:
            self.data = request_split[1]
    
        
    def createHTTPRequest(self,httpVersion= 1.0):
        request = self.method+" / HTTP/"+str(httpVersion)+"\r\nHost:"+self.host_name+"\r\n\r\n"
        return request



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
     
        