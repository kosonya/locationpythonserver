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
import math

class LocationEstimator(object):
    def __init__(self, minimum_p = 1e-20, debug = False):
        self.minimum_p = minimum_p
        self.debug = debug

    def pdf(self, x, avg, std):
        if std == 0:
            if x == avg:
                return 1
            else:
                return self.minimum_p
        return math.exp(- ((x - avg)**2) / (2.0*(std**2))   ) / (std*math.sqrt(2*math.pi)) 
        
    def wifi_probabilities(self, wifi_reading, wifi_stats):
        res = {}
        for location in wifi_stats.keys():
            p = 1
            for bssid in wifi_reading.keys():
                if wifi_stats[location].has_key(bssid):
                    avg, std = wifi_stats[location][bssid]["avg"], wifi_stats[location][bssid]["std"]
                    level = wifi_reading[bssid]
                    if self.debug:
                        print "level, avg, std", level, avg, std, "pdf", self.pdf(level, avg, std)
                    p *= self.pdf(level, avg, std)
                else:
                    p *= self.minimum_p
            if self.debug:
                print "total p:", p, "\n"
            res[location] = p
        return res
    
    def gps_probabilities(self, gps_reading, gps_stats):
        res = {}
        for location in gps_stats.keys():
            p = 1
            for key in ["lon", "lat"]:
                level = gps_reading[key]
                avg, std = gps_stats[location][key]["avg"], gps_stats[location][key]["std"]
                pdf = self.pdf(level, avg, std)
                if self.debug:
                    print key, "location:", location, "level:", level, "avg:", avg, "std:", std, "pdf:", pdf
                p *= pdf
            if self.debug:
                print "total GPS p:", p, "\n"
            res[location] = p
        return res
    
    def probabilities(self, wifi_reading, gps_reading, wifi_stats, gps_stats):
        if gps_reading == {} and wifi_reading == {}:
            return {}
        if gps_reading != {}:
            g = self.gps_probabilities(gps_reading, gps_stats)
            keys = g.keys()
        else:
            g = {}
        if wifi_reading != {}:
            w = self.wifi_probabilities(wifi_reading, wifi_stats)
            keys = w.keys()
        else:
            w = {}
        res = {}
        for location in keys:
                res[location] = 1
                if w != {}:
                    if res.has_key(location) and w.has_key(location):
                        res[location] *= w[location]
                if g != {}:
                    if res.has_key(location) and g.has_key(location):
                        res[location] *= g[location]
        return res
    
    
    def estimate_location(self, probabilities):
        return max(probabilities.items(), key = lambda x: x[1])
    
    def locations_list(self, probabilities):
        return sorted(probabilities.items(), key = lambda x: -x[1])
    
    
    
