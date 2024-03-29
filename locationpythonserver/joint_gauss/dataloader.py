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
import MySQLdb

def _connect():
    db = MySQLdb.connect(host = 'localhost', user = 'root', db = 'wifilocation')
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    return db, c

def get_all_locations():
    db, c = _connect()
    c.execute("SELECT location_id, location_name FROM locations")
    res = {}
    for (_id, name) in c.fetchall():
        res[int(_id)] = str(name)
    c.close()
    db.close()
    return res

def get_all_timestamps():
    db, c = _connect()
    c.execute("SELECT DISTINCT timestamp FROM wifi_readings")
    res = [int(x[0]) for x in c.fetchall()]
    c.close()
    db.close()
    return res

def get_all_bssids():
    db, c = _connect()
    c.execute("SELECT DISTINCT BSSID FROM wifi_readings")
    res = []
    for row in c.fetchall():
        res.append(str(row[0]))
    c.close()
    db.close()
    return res

def get_all_wifi_stats():
    db, c = _connect()
    c.execute("SELECT location_id, BSSID, AVG(level), STD(level) FROM wifi_readings WHERE location_id IN (SELECT location_id FROM locations) GROUP BY location_id, BSSID")
    res = {}
    for row in c.fetchall():
        location_id = int(row[0])
        bssid = row[1]
        if res.has_key(location_id):
            res[location_id][bssid] = (float(row[2]), float(row[3]))
        else:
            res[location_id] = {bssid : (float(row[2]), float(row[3]))}
    c.close()
    db.close()
    return res

def get_all_gps_stats():
    db, c = _connect()
    c.execute("SELECT location_id, AVG(Latitude), STD(Latitude), AVG(Longitude), STD(Longitude) FROM gps_and_signal_readings WHERE location_id IN (SELECT location_id FROM locations) GROUP BY location_id")
    res = {}
    for row in c.fetchall():
        location_id = int(row[0])
        res[location_id] = (float(row[1]), float(row[2]), float(row[3]), float(row[4]))
    c.close()
    db.close()
    return res

def get_one_wifi_reading(timestamp):
    db, c = _connect()
    c.execute("SELECT BSSID, level FROM wifi_readings WHERE timestamp = %d" % timestamp)
    res = {}
    for (bssid, level) in c.fetchall():
        res[bssid] = int(level)
    c.close()
    db.close()
    return res

def get_some_timestamp():
    db, c = _connect()
    c.execute("SELECT timestamp FROM wifi_readings LIMIT 1")
    res = int(c.fetchone()[0])
    c.close()
    db.close()
    return res

def get_few_timestamps(n):
    db, c = _connect()
    c.execute("SELECT DISTINCT timestamp FROM wifi_readings LIMIT %d" % n)
    res = [int(x[0]) for x in c.fetchall()]
    c.close()
    db.close()
    return res

def get_one_gps_reading(timestamp):
    db, c = _connect()
    c.execute("SELECT Latitude, Longitude FROM gps_and_signal_readings WHERE timestamp = %d" % timestamp)
    row = c.fetchone()
    res = float(row[0]), float(row[1])
    c.close()
    db.close()
    return res

def get_true_location(timestamp):
    db, c = _connect()
    c.execute("SELECT location_id FROM gps_and_signal_readings WHERE timestamp = %d" % timestamp)
    res = int(c.fetchone()[0])
    c.close()
    db.close()
    return res


def load_wifi_gps(timestamp):
    w = get_one_wifi_reading(timestamp)
    g = get_one_gps_reading(timestamp)
    return w, g

def main():
    print get_all_locations()
    for bssid in get_all_bssids():
        print bssid
    data = get_all_wifi_stats()
    for location in data.keys():
        print location
        for bssid in data[location].keys():
            print "\t", bssid, ":", data[location][bssid]
    print get_all_gps_stats()
    t = get_some_timestamp()
    print get_one_wifi_reading(t)
    print get_one_gps_reading(t)
    
if __name__ == "__main__":
    main()