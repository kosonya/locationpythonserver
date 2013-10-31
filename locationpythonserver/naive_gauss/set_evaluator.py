#!/usr/bin/env python

import dataloader
import dataprocessor
import traceback

def create_data_processor():
    wifi_stats = dataloader.get_all_wifi_stats()
    gps_stats = dataloader.get_all_gps_stats()
    dp = dataprocessor.DataProcessor(wifi_stats, gps_stats)
    return dp

def load_wifi_gps(timestamp):
    w = dataloader.get_one_wifi_reading(timestamp)
    g = dataloader.get_one_gps_reading(timestamp)
    return w, g

def main():
    dp = create_data_processor()
#    ts = dataloader.get_few_timestamps(10)
    ts = dataloader.get_all_timestamps()
    l = len(ts)
    rights = 0
    for i in xrange(l):
        try:
            t = ts[i]
            w, g = load_wifi_gps(t)
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