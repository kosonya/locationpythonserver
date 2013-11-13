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
                