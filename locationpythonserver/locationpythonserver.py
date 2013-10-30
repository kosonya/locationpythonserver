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
        query = "SELECT location_id FROM locations WHERE location_name = \'%s\'" % location
        while c.execute(query) != 1:
            c.execute("INSERT INTO locations (location_name) VALUES (\'%s\')" % location)
            db.commit()
        location_id = int(c.fetchone()[0])
        
        for key in obj.keys():
            if key[:9] == "wifiBSSID":
                bssid = key[9:]
                level = obj[key]
                print bssid, ":", level
                query = "INSERT INTO wifi_readings (timestamp, location_id, BSSID, level) VALUES (%d, %d, \'%s\', %d)" % (timestamp, location_id, bssid, level)
                print query
                r= c.execute(query)
                print "response:", r
                for l in c.fetchall():
                        print l
                print '\n'
        c.close()
        db.commit()
        db.close()
        print '\n'

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