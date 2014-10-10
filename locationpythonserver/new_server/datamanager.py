#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import MySQLdb
import bg_updater

class DataManager(object):
    
    def __init__(self, db_host = "localhost", db_user = "root", db_password = "12345",
                 db_name = "wifi_gps_readings", background_updates_delay = 10, debug = False):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.background_updates_delay = background_updates_delay
        self.debug = debug
        self.wifi_stats = {}
        self.gps_stats = {}
        self.fetch_all_from_db()
        
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
        self.bg_upd_thread = bg_updater.BackgroundUpdater(reference_class = self, delay = 10,
                                                          msg = "Wifi and GPS were updated",
                                                          debug = self.debug)
        self.bg_upd_thread.start()
        
    def fetch_all_from_db(self):
        self.get_all_gps_stats()
        self.get_all_wifi_stats()
    
    def get_all_wifi_stats(self):
        db, c = self.db_init()
        c.execute("SELECT location_id, BSSID, AVG(level), STD(level) FROM wifi_readings GROUP BY location_id, BSSID")
        for row in c.fetchall():
            location_id = int(row[0])
            bssid = unicode(row[1])
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
        c.execute("SELECT location_id, AVG(Latitude), STD(Latitude), AVG(Longitude), STD(Longitude) FROM gps_and_signal_readings GROUP BY location_id")
        for row in c.fetchall():
            location_id = int(row[0])
            self.gps_stats[location_id] = {"lat":
                                    {"avg": float(row[1]), "std": float(row[2])},
                                "lon":
                                    {"avg": float(row[3]), "std": float(row[4])}
                                }
        c.close()
        db.close()
        
    def _save_one_reading(self, timestamp, locid, wifi_data, gps_data, db, c):
        if wifi_data != {}:
            query_template = "INSERT INTO wifi_readings (timestamp, location_id, BSSID, level) VALUES (%s, %s, %s, %s)"
            for BSSID, level in wifi_data.items():
                c.execute(query_template, (timestamp, locid, BSSID, level))
        if gps_data != {}:
            query_template = "INSERT INTO gps_and_signal_readings (timestamp, location_id, Longitude, Latitude) VALUES (%s, %s, %s, %s)"
            c.execute(query_template, (timestamp, locid, gps_data["lon"], gps_data["lat"]))
            
    def save_one_reading(self, timestamp, locid, wifi_data, gps_data):
        db, c = self.db_init()
        self._save_one_reading(timestamp, locid, wifi_data, gps_data, db, c)
        c.close()
        db.commit()
        db.close()
        
    def load_one_reading(self, timestamp):
        db, c = self.db_init()
        query_template = "SELECT location_id, Longitude, Latitude FROM gps_and_signal_readings WHERE timestamp = %s"
        c.execute(query_template, (timestamp, ))
        res = c.fetchone()
        gps = {}
        locid = int(res[0])
        gps['lon'] = float(res[1])
        gps['lat'] = float(res[2])
        wifi = {}
        query_template = "SELECT BSSID, level FROM wifi_readings WHERE timestamp = %s AND location_id = %s"
        c.execute(query_template, (timestamp, locid))
        for BSSID, level in c.fetchall():
            wifi[str(BSSID)] = int(level)
        c.close()
        db.close()
        return timestamp, locid, wifi, gps
    
    def load_timestamps(self, limit = None):
        db, c = self.db_init()
        if not limit:
            query = "SELECT DISTINCT timestamp FROM gps_and_signal_readings"
            c.execute(query)
        else:
            query_template = "SELECT DISTINCT timestamp FROM gps_and_signal_readings LIMIT %s"
            c.execute(query_template, (limit, ))
        res = [int(row[0]) for row in c.fetchall()]
        c.close()
        db.close()
        return res

def main():
    dm = DataManager(debug = True)
    ts = dm.load_timestamps(limit = 10)
    for t in ts:
        print dm.load_one_reading(t)
    
if __name__ == "__main__":
    main()
        
        
    
