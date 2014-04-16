#!/usr/bin/env python
#    Copyright (c) 2013 Maxim Kovalev, Carnegie Mellon University
#    This file is part of Locationing Server.
#
#    Locationing Server is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Locationing Server is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Locationing Server.  If not, see <http://www.gnu.org/licenses/>.
import datamanager
import jsonparser
import locationresolver
import httplib
import json

def main():
    f = open("dump_training_2.txt", "r")
    dump = []
    for json_packet in f.readlines():
        #print json_packet
        try:
            json_obj = json.loads(json_packet)
            if not json_obj.has_key('location'):
                continue
            dump.append(json_obj)
        except Exception as e:
            print e

    print len(dump), "objects"
    rights = 0
    conn = httplib.HTTPConnection(host = "localhost", port = 8080)
    for i, json_obj in enumerate(dump):
        trueloc = json_obj['location']
        json_str = json.dumps(json_obj)
        print "Object", i+1, "out of", len(dump)
        print json_str
        conn.request("POST", "/api/v1/process_wifi_gps_reading/list/", json_str, {"Content-type": "application/json"})
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data
        try:
            loc = json.loads(response.reason)[0]['location_name']
            print "Sent location:", trueloc, "; received location:", loc
            if loc == trueloc:
                print "That's correct!"
                rights += 1
                print "Success rate so far:", float(rights)/(i+1)
        except Exception as e:
           pass
    print "Success rate:", float(rights)/len(dump)
        
        
        
if __name__ == "__main__":
    main()
