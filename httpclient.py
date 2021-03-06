#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse # for parsing urls

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):


    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = 500

        data_list = data.split()
        code = int(data_list[1])

        return code

    def get_headers(self,data):
        return None

    def get_body(self, data):
        body = ""
        i = 0

        while(i < len(data)):
            if(data[i:i+4] == "\r\n\r\n"):
                body = data[i+4:]
            i += 1

        return body

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def make_httprequest(self, command, url):
        httprequest = ""
        httpversion = "HTTP/1.1"
        parsed_url = urlparse(url)
        host = "localhost:{}".format(80 if(parsed_url.port == None) else parsed_url.port)
        content_length = 0
        method = ""
        headers = "Host: {}\r\nContent-Length: {}".format(host, content_length)
        body = ""

        if(command == "GET"):
            method = "{} {} {}".format(command, url, httpversion)
        elif(command == "POST"):
            method = "{} {} {}".format(command, url, httpversion)
            body = parsed_url.query

        httprequest = "{}\r\n{}\r\n\r\n{}".format(method, headers, body)

        return httprequest

    def get_response(self, request, url):
        code = 500
        body = ""
        parsed_url = urlparse(url)
        
        hostname = parsed_url.hostname
        port = 80 if(parsed_url.port == None) else int(parsed_url.port)
     
        self.connect(hostname, port)

        self.socket.sendall(request.encode())
        self.socket.shutdown(socket.SHUT_WR)

        http_response = self.recvall(self.socket)

        code = self.get_code(http_response)
        body = self.get_body(http_response)

        self.socket.close()
        
        return HTTPResponse(code, body)

    def GET(self, url, args=None):
        http_get_request = self.make_httprequest("GET", url)
        return self.get_response(http_get_request, url)

    def POST(self, url, args=None):
        http_post_request = self.make_httprequest("POST", url)
        return self.get_response(http_post_request, url)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

    
if __name__ == "__main__":
    client = HTTPClient()
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        command.init( sys.argv[2] )
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        command.init( sys.argv[1] )
        print(client.command( sys.argv[1] ))