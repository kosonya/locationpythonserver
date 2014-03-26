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
    for json_packet in f.readlines():
        print json_packet
        try:
            json_obj = json.loads(json_packet)
            if not json_obj.has_key('location'):
                continue
            print json_obj
        except Exception as e:
            print e
    print json_obj  
    
    
    return
    dm = datamanager.DataManager(debug = True, db_name="wifi_location_test")
    locres = locationresolver.LocationResolver(debug = True)
    jp = jsonparser.JsonParser(debug = True)
    
    ts = dm.load_timestamps()
    conn = httplib.HTTPConnection(host = "localhost", port = 8080)
    for timestamp in ts:
        _, locid, wifi_data, gps_data = dm.load_one_reading(timestamp)
        locname = locres.resolve_id(locid)
        json_str = jp.encode_wifi_gps(timestamp, locname, wifi_data, gps_data)
        print json_str
        conn.request("POST", "/api/v1/process_wifi_gps_reading/list/", json_str, {"Content-type": "application/json"})
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data
        
        
        
if __name__ == "__main__":
    main()
