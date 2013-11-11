#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import threading

class DataManager(object):
    
    def __init__(self, db_host = "localhost", db_user = "root", db_password = "",
                 db_name = "wifilocation", background_updates_delay = 10, debug = False):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.background_updates_delay = background_updates_delay
        self.debug = debug
        self.wifi_stats = {}
        self.gps_stats = {}
        
    def db_init(self):
        db = MySQLdb.connect(host = self.db_host, user = self.db_user,
                             passwd = self.db_password , db = self.db_name)
        db.set_character_set('utf8')
        c = db.cursor()
        c.execute('SET NAMES utf8')
        c.execute('SET CHARACTER SET utf8')
        c.execute('SET character_set_connection=utf8')
        return db, c
    
    def start_background_updates(self):
        def update(main_class):
            while True:
                main_class.fetch_all_from_db()
                if self.debug:
                    print "Location list updated! Sleeping for {} seconds".format(self.background_updates_delay)
                time.sleep(self.background_updates_delay)
            
        self.bg_upd_thread = threading.Thread(target = update, args = [self])
        self.bg_upd_thread.daemon = True
        self.bg_upd_thread.start()
        
    def fetch_all_from_db(self):
        pass
    
    def get_all_wifi_stats(self):
        db, c = self.db_init()
        c.execute("SELECT location_id, BSSID, AVG(level), STD(level) FROM wifi_readings WHERE location_id IN (SELECT location_id FROM locations) GROUP BY location_id, BSSID")
        for row in c.fetchall():
            location_id = int(row[0])
            bssid = row[1]
            if self.wifi_stats.has_key(location_id):
                self.wifi_stats[location_id][bssid] = {"avg": float(row[2]),
                                                       "std": float(row[3])
                                                       }
            else:
                self.wifi_stats[location_id] = {bssid : {"avg": float(row[2]),
                                                         "std": float(row[3])
                                                         }
                                                }
        c.close()
        db.close()
    
    def get_all_gps_stats(self):
        db, c = self.db_init()
        c.execute("SELECT location_id, AVG(Latitude), STD(Latitude), AVG(Longitude), STD(Longitude) FROM gps_and_signal_readings WHERE location_id IN (SELECT location_id FROM locations) GROUP BY location_id")
        res = {}
        for row in c.fetchall():
            location_id = int(row[0])
            res[location_id] = {"lat":
                                    {"avg": float(row[1]), "std": float(row[2])},
                                "lon":
                                    {"avg": float(row[3]), "std": float(row[4])}
                                }
        c.close()
        db.close()
        return res

def main():
    pass
    
if __name__ == "__main__":
    main()
        
        
    