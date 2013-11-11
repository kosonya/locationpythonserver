#!/usr/bin/env python

import datamanager
import jsonparser
import locationresolver

def main():
    dm = datamanager.DataManager(debug = True)
    locres = locationresolver.LocationResolver(debug = True)
    jp = jsonparser.JsonParser(debug = True)
    
    ts = dm.load_timestamps(limit = 10)
    for timestamp in ts:
        _, locid, wifi_data, gps_data = dm.load_one_reading(timestamp)
        locname = locres.resolve_id(locid)
        json_str = jp.encode_wifi_gps(timestamp, locname, wifi_data, gps_data)
        print json_str
        
if __name__ == "__main__":
    main()