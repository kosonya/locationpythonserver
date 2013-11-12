#!/usr/bin/env python

import datamanager
import jsonparser
import locationresolver
import httplib

def main():
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
        conn.request("POST", "/api/v1/process_wifi_gps_reading/", json_str, {"Content-type": "application/json"})
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data
        
        
        
if __name__ == "__main__":
    main()