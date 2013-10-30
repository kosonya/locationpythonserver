#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import cgi
import json
import MySQLdb

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
        obj = json.loads(data.keys()[0])
        timestamp = obj['timestamp']
        print 'Timestamp:', timestamp
        location = obj['location']
        print location
        db = MySQLdb.connect(host = 'localhost', user = 'root', db = 'wifilocation')
        c = db.cursor()
        for key in obj.keys():
            if key[:9] == "wifiBSSID":
                bssid = key[9:]
                level = obj[key]
                print bssid, ":", level
                query = "INSERT INTO readings (timestamp, location, BSSID, level) VALUES (%d, \'%s\', \'%s\', %d)" % (timestamp, location, bssid, level)
                c.execute(query)
        c.close()
        db.close()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
 
    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)
 
class SimpleHttpServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
 
    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = False
        self.server_thread.start()
 
    def waitForThread(self):
        self.server_thread.join()
 
    def stop(self):
        self.server.shutdown()
        self.waitForThread()


def main():
    server = SimpleHttpServer('', 8080)
    print 'HTTP Server Running...........'
    server.start()
    server.waitForThread()
    
if __name__ == "__main__":
    main()