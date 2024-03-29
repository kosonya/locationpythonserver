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
    f = open("dump_test_2.txt", "r")
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
    dump_len = len(dump)
    rights = 0
    conn = httplib.HTTPConnection(host = "localhost", port = 8080)
    by_location = {}
    by_device = {}
    for i, json_obj in enumerate(dump):
        trueloc = json_obj['location']
        dev = json_obj['device_model']
        del json_obj['location']
	should_continue = True
	no_gps = False
	no_wifi = False
	if no_wifi:
		for key in json_obj.keys():
			if "wifi" in key:
				del json_obj[key]
			elif "GPS" in key:
				should_continue = False
		if should_continue:
			dump_len -= 1
			continue
	elif no_gps:
		for key in json_obj.keys():
			if "GPS" in key:
				del json_obj[key]
			elif "wifi" in key:
				should_continue = False
		if should_continue:
			dump_len -= 1
			continue
        json_str = json.dumps(json_obj)
        print "Object", i+1, "out of", len(dump)
        print json_str
        conn.request("POST", "/api/v1/process_wifi_gps_reading/list/", json_str, {"Content-type": "application/json"})
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        if by_location.has_key(trueloc):
            by_location[trueloc][0] += 1
        else:
            by_location[trueloc] = [1, 0]
        if by_device.has_key(dev):
            by_device[dev][0] += 1
        else:
            by_device[dev] = [1, 0]
        print data
        try:
            loc = json.loads(response.reason)[0]['location_name']
            print "Sent location:", trueloc, "; received location:", loc
            if loc == trueloc:
                print "That's correct!"
                rights += 1
                by_location[trueloc][1] += 1
                by_device[dev][1] += 1
                print "Success rate so far:", float(rights)/(i+1)
        except Exception as e:
           pass
    print "Success rate:", float(rights)/dump_len
    print "\n\n"
    for loc in by_location.keys():
        print loc, "&", by_location[loc][0], "&", ("%3.1f\%%\\\\" % (100*float(by_location[loc][1])/by_location[loc][0]))
        print ""#"\\hline"
    #print "Total &", 
    print dump_len, "&", ("%3.1f\%%\\\\" % (100*float(rights)/dump_len))
    print "\n\n"
    for dev in by_device.keys():
        #print dev, "&", 
	print by_device[dev][0], "&", ("%3.1f\%%\\\\" % (100*float(by_device[dev][1])/by_device[dev][0]))
        print ""#"\\hline"
    #print "Total &", 
    print dump_len, "&", ("%3.1f\%%\\\\" % (100*float(rights)/dump_len))
        
if __name__ == "__main__":
    main()
