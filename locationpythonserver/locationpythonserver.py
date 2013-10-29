#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

class HTTPRequestHandler(BaseHTTPRequestHandler):
 
    def do_POST(self):
        print "Path:", self.path
        ctype, _ = cgi.parse_header(self.headers.getheader('content-type'))
        print "ctype:", ctype
        length = int(self.headers.getheader('content-length'))
        print "Length:", length
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        print "Data:", data
        self.send_response(200, "Roger that")




def main():
    print "Hello"
    
if __name__ == "__main__":
    main()