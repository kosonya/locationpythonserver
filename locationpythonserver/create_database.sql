DROP DATABASE IF EXISTS `wifilocation`;
CREATE DATABASE `wifilocation`;
USE `wifilocation`;

DROP TABLE IF EXISTS `gps_and_signal_readings`;
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


DROP TABLE IF EXISTS `locations`;
CREATE TABLE `locations` (
  `location_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `location_name` varchar(255) NOT NULL,
  PRIMARY KEY (`location_id`),
  UNIQUE KEY `location_name_UNIQUE` (`location_name`),
  KEY `location_id_wifi` (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `wifi_readings`;
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
) ENGINE=InnoDB AUTO_INCREMENT=255 DEFAULT CHARSET=utf8;
