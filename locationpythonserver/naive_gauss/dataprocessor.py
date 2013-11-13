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



class DataProcessor(object):
    def __init__(self, wifi_stats, gps_stats, minimum_p = 1e-5):
        self.wifi_stats = wifi_stats
        self.gps_stats = gps_stats
        self.minimum_p = minimum_p

    def pdf(self, x, avg, std):
        if std == 0:
            if x == avg:
                return 1
            else:
                return self.minimum_p
        return math.exp(- ((x - avg)**2) / (2.0*(std**2))   ) / (std*math.sqrt(2*math.pi)) 
        
    def wifi_probabilities(self, wifi_reading):
        res = {}
        for location in self.wifi_stats.keys():
            p = 1
            for bssid in wifi_reading.keys():
                if self.wifi_stats[location].has_key(bssid):
                    avg, std = self.wifi_stats[location][bssid]
                    level = wifi_reading[bssid]
#                    print "level, avg, std", level, avg, std, "pdf", self.pdf(level, avg, std)
                    p *= self.pdf(level, avg, std)
                else:
                    p *= self.minimum_p
#            print "total p:", p, "\n"
            res[location] = p
        return res
    
    def gps_probabilities(self, gps_reading):
        res = {}
        for location in self.gps_stats.keys():
            p = 1
            for i in [0, 1]:
                avg, std = self.gps_stats[location][2*i], self.gps_stats[location][2*i+1]
                level = gps_reading[i]
#                print "level, avg, std", level, avg, std
#                print "self.pdf(level, avg, std)", self.pdf(level, avg, std)
                p *= self.pdf(level, avg, std)
#            print "total GPS p:", p, "\n"
            res[location] = p
        return res
    
    def probabilities(self, wifi_reading, gps_reading):
        w = self.wifi_probabilities(wifi_reading)
        g = self.gps_probabilities(gps_reading)
        res = {}
        for location in w.keys():
                res[location] = w[location] * g[location]
        return res
    
    
    def estimate_location(self, wifi_reading, gps_reading):
        ps = self.probabilities(wifi_reading, gps_reading)
        return max(ps.items(), key = lambda x: x[1])
    
    