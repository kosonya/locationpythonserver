#!/usr/bin/env python

import math

def pdf(x, avg, std):
    return math.exp(- ((x - avg)**2) / (2.0*(std**2))) / (std*math.sqrt(2*math.pi))

class DataProcessor(object):
    def __init__(self, wifi_stats, gps_stats, minimum_p = 1e-5):
        self.wifi_stats = wifi_stats
        self.gps_stats = gps_stats
        self.minimum_p = minimum_p
        
    def wifi_probabilities(self, wifi_reading):
        res = {}
        for location in self.wifi_stats.keys():
            p = 1
            for bssid in wifi_reading.keys():
                if self.wifi_stats[location].has_key(bssid):
                    avg, std = self.wifi_stats[location][bssid]
                    level = wifi_reading[bssid]
                    p *= pdf(level, avg, std)
                else:
                    p *= self.minimum_p
            res[location] = p
        return res
    
    def gps_probabilities(self, gps_reading):
        res = {}
        for location in self.gps_stats.keys():
            p = 1
            for i in [0, 1]:
                avg, std = self.gps_stats[location][i+1], self.gps_stats[location][i+2]
                level = gps_reading[i]
                p *= pdf(level, avg, std)
            res[location] = p
        return res
    
    def probabilities(self, wifi_reading, gps_reading):
        return self.wifi_probabilities(wifi_reading) * self.gps_probabilities(gps_reading)
    
    def estimate_location(self, wifi_reading, gps_reading):
        ps = self.probabilities(wifi_reading, gps_reading)
        return max(ps.items(), key = lambda x: x[1])
    
    