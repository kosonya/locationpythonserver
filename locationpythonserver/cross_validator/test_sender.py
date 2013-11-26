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
    dm = datamanager.DataManager(debug = True, db_name="wifi_gps_readings")
    locres = locationresolver.LocationResolver(debug = True)
    jp = jsonparser.JsonParser(debug = True)
    
    ts = dm.load_timestamps()
    conn = httplib.HTTPConnection(host = "localhost", port = 8080)
    l = len(ts)
    rights = 0.0
    for i in xrange(l):
        timestamp = ts[i]
        _, locid, wifi_data, gps_data = dm.load_one_reading(timestamp)
        locname = locres.resolve_id(locid)
        json_str = jp.encode_wifi_gps(timestamp, locname, wifi_data, gps_data)
        print json_str
        conn.request("POST", "/api/v1/process_wifi_gps_reading/list/", json_str, {"Content-type": "application/json"})
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data
        print "Reading {} of {}".format(i, l)
        try:
            	j = json.loads(response.reason)
                loc = j[0]["location_name"]
                print "Sent:", locname, "received:", loc
                if loc == locname:
                    rights += 1.0
                    print "That's right!"
        except Exception as e:
                print e
        print "Current success rate:", rights/float(i+1)
    print "Success rate:", rights/float(l)
        
        
        
if __name__ == "__main__":
    main()
