DROP DATABASE IF EXISTS `location_resolve`;
CREATE DATABASE `location_resolve`;
USE `location_resolve`;

DROP TABLE IF EXISTS `locations`;
CREATE TABLE `locations` (
  `location_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `location_name` varchar(255) NOT NULL,
  PRIMARY KEY (`location_id`),
  UNIQUE KEY `location_name_UNIQUE` (`location_name`),
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;