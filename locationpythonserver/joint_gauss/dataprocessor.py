#!/usr/bin/env python

#Gaussian code from http://lmf-ramblings.blogspot.com/2009/07/multivariate-normal-distribution-in.html

import numpy





class DataProcessor(object):
    def __init__(self, all_bssids, all_locations, minimum_p = 1e-5, minimum_dbm = -101, dtype = "float64"):
        self.all_bssids = all_bssids
        self.minimum_p = minimum_p
        self.minimum_dbm = minimum_dbm
        self.dtype = dtype
        self.joint_readings = {}
        self.all_locations = all_locations

    def pdf(self, b, location):
        cov, mean = self.covmean[location]
        print "cov", cov
        print "mean", mean
        print "b", b
        k = b.shape[0]
        part1 = numpy.exp(-0.5*k*numpy.log(2*numpy.pi))
        part2 = numpy.power(numpy.linalg.det(cov),-0.5)
        dev = b-mean
        part3 = numpy.exp(-0.5*numpy.dot(numpy.dot(dev.transpose(),numpy.linalg.inv(cov)),dev))
        dmvnorm = part1*part2*part3 
        return dmvnorm

    def build_wifi_features_single(self, wifi_reading):
        res = []
        for bssid in self.all_bssids:
            if wifi_reading.has_key(bssid):
                res.append(wifi_reading[bssid])
            else: res.append(self.minimum_dbm)
        return res
    
    def build_gps_features_single(self, gps_reading):
        return list(gps_reading)
    
    def build_all_features_single(self, wifi_reading, gps_reading):
        w = self.build_wifi_features_single(wifi_reading)
        g = self.build_gps_features_single(gps_reading)
        return numpy.array(w + g, dtype=self.dtype)
    
    def add_reading(self, wifi_reading, gps_reading, location):
        arr = self.build_all_features_single(wifi_reading, gps_reading)
        if self.joint_readings.has_key(location):
            self.joint_readings[location] = numpy.vstack( (self.joint_readings[location], arr) )
        else:
            self.joint_readings[location] = arr
    
    def compute_cov_mean(self):
        self.covmean = {}
        for location in self.joint_readings.keys():
            T = numpy.transpose(self.joint_readings[location])
            covariance = numpy.cov(T)
            mean = numpy.mean(T, axis = 1)
            self.covmean[location] = (covariance, mean)
 
    def probabilities(self, wifi_reading, gps_reading):
        vector = self.build_all_features_single(wifi_reading, gps_reading)
        res = {}
        for location in self.covmean.keys():
                res[location] = self.pdf(vector, location)
        return res
    
    
    def estimate_location(self, wifi_reading, gps_reading):
        ps = self.probabilities(wifi_reading, gps_reading)
        return max(ps.items(), key = lambda x: x[1])
    
    