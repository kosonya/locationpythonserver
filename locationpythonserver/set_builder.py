#!/usr/bin/env python

import MySQLdb
import random

def create_db(db_name):
    create_tables = """
    CREATE TABLE `gps_and_signal_readings` (
      `reading_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
      `timestamp` bigint(20) NOT NULL,
      `location_id` int(10) unsigned NOT NULL,
      `Longitude` double NOT NULL,
      `Latitude` double NOT NULL,
      `Cellular_signal` int(11) DEFAULT NULL,
      PRIMARY KEY (`reading_id`),
      KEY `location` (`location_id`),
      KEY `timestamp` (`timestamp`),
      KEY `locationtimestamp` (`location_id`,`timestamp`),
      KEY `timestamplocation` (`timestamp`,`location_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    CREATE TABLE `locations` (
      `location_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
      `location_name` varchar(255) NOT NULL,
      PRIMARY KEY (`location_id`),
      UNIQUE KEY `location_name_UNIQUE` (`location_name`),
      KEY `location_id_wifi` (`location_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
    CREATE TABLE `wifi_readings` (
      `reading_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
      `timestamp` bigint(20) unsigned NOT NULL,
      `location_id` int(10) unsigned NOT NULL,
      `BSSID` varchar(17) NOT NULL,
      `level` int(11) NOT NULL,
      PRIMARY KEY (`reading_id`),
      UNIQUE KEY `reading_id_UNIQUE` (`reading_id`) USING BTREE,
      KEY `BSSID` (`BSSID`),
      KEY `BSSID_timestamp` (`BSSID`,`timestamp`),
      KEY `timestamp_BSSID` (`timestamp`,`BSSID`),
      KEY `location` (`location_id`),
      KEY `location_timestamp` (`location_id`,`timestamp`),
      KEY `timestamp_location` (`timestamp`,`location_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=255 DEFAULT CHARSET=utf8
    """
    db = MySQLdb.connect(host='localhost', user='root')
    c = db.cursor()
    c.execute("DROP DATABASE IF EXISTS `%s`" % db_name)
    c.execute("CREATE DATABASE `%s`" % db_name)
    c.execute("USE `%s`" % db_name)
    for query in create_tables.split(';'):
        c.execute(query)
    c.close()
    db.commit()
    db.close()
    


def _connect(db):
    db = MySQLdb.connect(host = 'localhost', user = 'root', db = db)
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    return db, c

def get_all_timestamps(c):
    c.execute("SELECT DISTINCT timestamp FROM wifi_readings")
    res = [int(x[0]) for x in c.fetchall()]
    return res

def get_one_wifi_reading(timestamp, c):
    c.execute("SELECT BSSID, level FROM wifi_readings WHERE timestamp = %d" % timestamp)
    res = {}
    for (bssid, level) in c.fetchall():
        res[bssid] = int(level)
    return res

def get_one_gps_reading(timestamp, c):
    c.execute("SELECT Latitude, Longitude FROM gps_and_signal_readings WHERE timestamp = %d" % timestamp)
    row = c.fetchone()
    res = float(row[0]), float(row[1])
    return res

def get_true_location(timestamp, c):
    c.execute("SELECT location_id FROM gps_and_signal_readings WHERE timestamp = %d" % timestamp)
    res = int(c.fetchone()[0])
    return res

def process_one_reading(timestamp, wifi, gps, loc, c, db):
    query = "SELECT location_id FROM locations WHERE location_name = \'%s\'" % loc
    while c.execute(query) != 1:
        c.execute("INSERT INTO locations (location_name) VALUES (\'%s\')" % loc)
        db.commit()
    location_id = int(c.fetchone()[0])
    for bssid in wifi.keys():
        level = wifi[bssid]
        query = "INSERT INTO wifi_readings (timestamp, location_id, BSSID, level) VALUES (%d, %d, \'%s\', %d)" % (timestamp, location_id, bssid, level)
#       print query
        c.execute(query)
    query = "INSERT INTO gps_and_signal_readings (timestamp, location_id, Longitude, Latitude) VALUES (%d, %d, %f, %f)" % (timestamp, location_id, gps[1], gps[0])
#   print query
    c.execute(query)

def lookup_location(location_id, c):
    c.execute("SELECT location_name FROM locations WHERE location_id = %d" % location_id)
    res = c.fetchone()[0]
    return res  

def main():
    test_ratio = 0.2
    print "Creating dbs"
    create_db("wifi_location_training")
    create_db("wifi_location_test")
    print "Created"
    src_db, src_c = _connect("wifilocation")
    test_db, test_c = _connect("wifi_location_test")
    training_db, training_c = _connect("wifi_location_training")
    timestamps = get_all_timestamps(src_c)
    l = len(timestamps)
    for i in xrange(l):
        timestamp = timestamps[i]
        print "Processing", i, "of", l, "(", 100*i/l, "%)"
        wifi = get_one_wifi_reading(timestamp, src_c)
        gps = get_one_gps_reading(timestamp, src_c)
        loc = lookup_location(get_true_location(timestamp, src_c), src_c)
        (db, c) =  (test_db, test_c) if random.uniform(0, 1) < test_ratio else (training_db, training_c)
        process_one_reading(timestamp, wifi, gps, loc, c, db)
    test_c.close()
    test_db.commit()
    training_c.close()
    training_db.commit()
    
if __name__ == "__main__":
    main()
    