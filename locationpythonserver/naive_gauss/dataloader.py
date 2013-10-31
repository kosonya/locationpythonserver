#!/usr/bin/env python

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
    
if __name__ == "__main__":
    main()