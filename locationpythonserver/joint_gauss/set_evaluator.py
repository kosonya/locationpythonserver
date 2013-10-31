#!/usr/bin/env python

import dataloader
import dataprocessor
import traceback

class UsefulData(object):
    def __init__(self):
        print "Getting all locations"
        self.all_locations = dataloader.get_all_locations()
        print "Getting all BSSIDs"
        self.all_bssids = dataloader.get_all_bssids()
        print "Getting all timestamps"
        #self.all_timestamps = dataloader.get_all_timestamps()
        self.all_timestamps = dataloader.get_few_timestamps(10)
        print "Got!"

def learn(ud):
    print "Learning"
    dp = dataprocessor.DataProcessor(ud.all_bssids, ud.all_locations)
    _l = len(ud.all_timestamps)
    for i in xrange(_l):
        t = ud.all_timestamps[i]
        print "Processing", i, "of", _l, "(", 100*i/_l, "%):", t
        l = dataloader.get_true_location(t)
        w = dataloader.get_one_wifi_reading(t)
        g = dataloader.get_one_gps_reading(t)
        dp.add_reading(w, g, l)
    dp.compute_cov_mean()
    return dp
        

def main():
    ud = UsefulData()
    dp = learn(ud)
    ts = ud.all_timestamps
    l = len(ts)
    rights = 0
    for i in xrange(l):
        try:
            t = ts[i]
            w, g = dataloader.load_wifi_gps(t)
            ev_loc = dp.estimate_location(w, g)
            tr_loc = dataloader.get_true_location(t)
            if ev_loc[0] == tr_loc:
                rights += 1
            print i, "of", l, "(", 100*i/l, "%), rights:", float(rights) / (i+1), "Timestamp:", t, "estimate:", ev_loc, "true:", tr_loc
        except Exception as e:
            tr = traceback.format_exc().splitlines()
            for line in tr:
                print line
            print e
            
        
    print "Total accuracy:", 100*float(rights) / l
    print "Or, considering i's", 100*float(rights) / (i+1)
 
if __name__ == "__main__":
    main()