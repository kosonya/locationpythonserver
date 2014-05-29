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
    f = open("dump.txt", "r")
    stats = {}
    stats_loc = {}
    total = 0
    rights = 0
    for json_packet in f.readlines():
        #print json_packet
        try:
            json_obj = json.loads(json_packet)
            if not json_obj.has_key('location'):
                continue
            print json_obj
            conn = httplib.HTTPConnection(host = "localhost", port = 8080)
            conn.request("POST", "/api/v1/process_wifi_gps_reading/", json_packet, {"Content-type": "application/json"})
            response = conn.getresponse()
            resp = json.loads(response.reason)
            total += 1
            
            if json_obj.has_key("device_model"):
                model = json_obj["device_model"]
            else:
                model = "undefined model"
            if stats.has_key(model):
                stats[model]["total"] += 1
            else:
                stats[model] = {"total": 1, "rights": 0}
                
                
            if stats_loc.has_key(json_obj["location"]):
                stats_loc[json_obj["location"]]["total"] += 1
            else:
                stats_loc[json_obj["location"]] = {"total": 1, "rights": 0}
        except Exception as e:
            print e


    
    print "Total entries: %d, success rate: %3.1f%%" % (total, 100*float(rights)/float(total))        
    for model in stats.keys():
        success = 100*float(stats[model]["rights"])/float(stats[model]["total"])
        print "Model: %s, entries: %d, success rate: %3.1f%%" % (model, stats[model]["total"], success)
 
    for loc in stats_loc.keys():
        success = 100*float(stats_loc[loc]["rights"])/float(stats_loc[loc]["total"])
        print "Location: %s, entries: %d, success rate: %3.1f%%" % (loc, stats_loc[loc]["total"], success)
if __name__ == "__main__":
    main()
