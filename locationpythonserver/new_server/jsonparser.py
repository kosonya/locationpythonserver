#!/usr/bin/env python

import json

class JsonParser(object):
    def __init__(self, debug = False):
        self.debug = debug
    
    def parse_wifi_gps_json(self, json_str):
        obj = json.loads(json_str)
        if isinstance(obj, list):
            raise Exception("Lists are not supported right now")
        
        if isinstance(obj, dict):
            timestamp = obj['timestamp']
            locname = obj['location']
            if self.debug:
                print timestamp, locname
            wifi_data = {}
            for key in obj.keys():
                if key[:9] == "wifiBSSID":
                    bssid = key[9:]
                    level = obj[key]
                    wifi_data[bssid] = level
            if not obj.has_key("GPSLat") or not obj.has_key("GPSLon"):
                gps_data = {}
            else:
                gps_data = {"lat": obj["GPSLat"],
                            "lon": obj["GPSLon"]
                            }
            return timestamp, locname, wifi_data, gps_data
                