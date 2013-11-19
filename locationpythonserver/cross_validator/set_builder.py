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


def main():
    test_ratio = 0.2
    print "Creating dbs"
    create_db("wifi_location_training_set")
    create_db("wifi_location_test_set")
    print "Created"
    src_db, src_c = _connect("wifi_gps_readings")
    test_db, test_c = _connect("wifi_location_test_set")
    training_db, training_c = _connect("wifi_location_training")
    timestamps = get_all_timestamps(src_c)
    l = len(timestamps)
    for i in xrange(l):
        timestamp = timestamps[i]
        print "Processing", i, "of", l, "(", 100*i/l, "%)"
        db, c =  (test_db, test_c) if random.uniform(0, 1) < test_ratio else (training_db, training_c)
	src_c.execute("SELECT timestamp, location_id, BSSID, level FROM wifi_readings WHERE timestamp = %s", timestamp)
	for timestamp, location_id, BSSID, level in src_c.fetchall():
		c.execute("INSERT INTO wifi_readings (timestamp, location_id, BSSID, level) VALUES (%s, %s, %s, %s)", (timestamp, location_id, BSSID, level))
	src_c.execute("SELECT Latitude, Longitude FROM gps_and_signal_readings WHERE timestamp = %s", timestamp)
	res = src_c.fetchone()
	if res:
		lat, lon = res
		c.execute("INSERT INTO gps_and_signal_readings (timestamp, location_id, Longitude, Latitude) VALUES (%s, %s, %s, %s)", (timestamp, location_id, lat, lon))
    test_c.close()
    test_db.commit()
    training_c.close()
    training_db.commit()
    
if __name__ == "__main__":
    main()
    
