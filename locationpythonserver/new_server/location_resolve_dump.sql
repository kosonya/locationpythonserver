-- MySQL dump 10.13  Distrib 5.5.34, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: location_resolve
-- ------------------------------------------------------
-- Server version	5.5.34-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `locations` (
  `location_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `location_name` varchar(255) NOT NULL,
  PRIMARY KEY (`location_id`),
  UNIQUE KEY `location_name_UNIQUE` (`location_name`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` VALUES (48,'b19 hall 1020-30'),(49,'b19 hall 1050-60'),(27,'B19 R1020'),(26,'B19 R1021'),(5,'B19 R1022 (Smart Spaces)'),(28,'B19 R1023 (Quiet room)'),(42,'B19 R1024'),(37,'B19 R1025'),(33,'B19 R1026'),(36,'B19 R1027'),(34,'B19 R1028'),(35,'B19 R1029'),(45,'B19 R1031'),(44,'B19 R1034'),(39,'B19 R1039'),(38,'B19 R1040'),(8,'B19 R1040 (activity room)'),(40,'B19 R1041'),(24,'B19 R1050'),(23,'B19 R1051'),(6,'B19 R1053 (kitchen)'),(29,'B19 R1058 '),(41,'B19 R1059'),(46,'B19 R1060'),(30,'B19 R1061 (Martin\'s office)'),(25,'B19 R1065'),(22,'B23 first floor hallway near R109/110'),(11,'B23 first floor kitchen'),(32,'B23 first floor lounge'),(12,'B23 main entrance'),(21,'B23 R109/110'),(10,'B23 R118'),(7,'B23 R129B'),(15,'B23 R211'),(14,'B23 R212'),(47,'B23 R214B'),(17,'B23 R228'),(16,'B23 second floor hallway near R211 and R212'),(13,'B23 second floor hallway near whiteboard'),(19,'B23 second floor kitchen'),(18,'B23 second floor lounge near stairs'),(20,'B23 second hallway near Rainbow printer'),(9,'Bus stop near B19');
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-12-20 13:47:37
