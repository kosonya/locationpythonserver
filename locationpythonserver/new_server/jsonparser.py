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
            if obj.has_key("location"):
                locname = obj['location']
            else:
                locname = None
            if self.debug:
                if locname:
                    print timestamp, locname
                else:
                    print timestamp, "No location"
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
        
    def encode_wifi_gps(self, timestamp, locname, wifi_data, gps_data):
        res = {"id": "fake_sender", "timestamp": timestamp, "location": locname}
        for BSSID, level in wifi_data.items():
            res["wifiBSSID%s" % BSSID] = level
        res["GPSLat"] = gps_data["lat"]
        res["GPSLon"] = gps_data["lon"]
        res_str = json.dumps(res)
        return res_str
                