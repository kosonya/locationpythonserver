#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import cgi
import json
import MySQLdb




def _process_one_obj(obj, db, c):
    timestamp = obj['timestamp']
    print 'Timestamp:', timestamp
    location = obj['location']
    print location
    query = "SELECT location_id FROM locations WHERE location_name = \'%s\'" % location
    while c.execute(query) != 1:
        c.execute("INSERT INTO locations (location_name) VALUES (\'%s\')" % location)
        db.commit()
    location_id = int(c.fetchone()[0])    
    for key in obj.keys():
        if key[:9] == "wifiBSSID":
            bssid = key[9:]
            level = obj[key]
#            print bssid, ":", level
            query = "INSERT INTO wifi_readings (timestamp, location_id, BSSID, level) VALUES (%d, %d, \'%s\', %d)" % (timestamp, location_id, bssid, level)
#            print query
            c.execute(query)

    if obj.has_key("GPSLat"):
        if obj.has_key("Cellular_signal"):
            query = "INSERT INTO gps_and_signal_readings (timestamp, location_id, Longitude, Latitude, Cellular_signal) VALUES (%d, %d, %f, %f, %d)" % (timestamp, location_id, obj['GPSLon'], obj['GPSLat'], obj['Cellular_signal'])
        else:
            query = "INSERT INTO gps_and_signal_readings (timestamp, location_id, Longitude, Latitude) VALUES (%d, %d, %f, %f)" % (timestamp, location_id, obj['GPSLon'], obj['GPSLat'])
#        print query
        c.execute(query)


def process_one_obj(obj):
    db = MySQLdb.connect(host = 'localhost', user = 'root', db = 'wifilocation_test')
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    _process_one_obj(obj, db, c)
    c.close()
    db.commit()
    db.close()

def process_several_objs(objs):
    db = MySQLdb.connect(host = 'localhost', user = 'root', db = 'wifilocation_test')
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    for o in objs:
        _process_one_obj(o, db, c)
    c.close()
    db.commit()
    db.close()

class HTTPRequestHandler(BaseHTTPRequestHandler):
 
    def address_string(self): #Fix for the slow response
        host, port = self.client_address[:2]
        #return socket.getfqdn(host)
        return host
 
    def do_POST(self):
        print "Path:", self.path
        ctype, _ = cgi.parse_header(self.headers.getheader('content-type'))
        print "ctype:", ctype
        length = int(self.headers.getheader('content-length'))
        print "Length:", length
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        #print "Data:", data
        self.send_response(200, "Roger that")
        obj = json.loads(data.keys()[0])
        if isinstance(obj, list):
            print "Processing a list"
            t = threading.Thread(target = process_several_objs, args = [obj])
            t.start()
        elif isinstance(obj, dict) and obj.has_key('timestamp') and obj.has_key('location'):
            print "Processing single dict"
            t = threading.Thread(target = process_one_obj, args = [obj])
            t.start()
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