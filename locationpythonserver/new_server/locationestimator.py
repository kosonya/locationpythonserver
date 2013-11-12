#!/usr/bin/env python

import math

class LocationEstimator(object):
    def __init__(self, minimum_p = 1e-5, debug = False):
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
        w = self.wifi_probabilities(wifi_reading, wifi_stats)
        g = self.gps_probabilities(gps_reading, gps_stats)
        res = {}
        for location in w.keys():
                res[location] = w[location] * g[location]
        return res
    
    
    def estimate_location(self, probabilities):
        return max(probabilities.items(), key = lambda x: x[1])
    
    
    