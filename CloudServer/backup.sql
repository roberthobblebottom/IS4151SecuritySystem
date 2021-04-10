/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
 
--
-- Table structure for table `authentication`
--
 
DROP TABLE IF EXISTS `authentication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authentication` (
  `adminid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`adminid`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
 
--
-- Dumping data for table `authentication`
--
 
LOCK TABLES `authentication` WRITE;
/*!40000 ALTER TABLE `authentication` DISABLE KEYS */;
INSERT INTO `authentication` VALUES (1,'admin','password');
/*!40000 ALTER TABLE `authentication` ENABLE KEYS */;
UNLOCK TABLES;
 
--
-- Table structure for table `authorisedentry`
--
 
DROP TABLE IF EXISTS `authorisedentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authorisedentry` (
  `idauthorisedentry` int NOT NULL AUTO_INCREMENT,
  `passcode` varchar(45) NOT NULL,
  `authoriserequestdate` datetime NOT NULL,
  `authoriseapprovedate` datetime DEFAULT NULL,
  PRIMARY KEY (`idauthorisedentry`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
 
--
-- Dumping data for table `authorisedentry`
--
 
LOCK TABLES `authorisedentry` WRITE;
/*!40000 ALTER TABLE `authorisedentry` DISABLE KEYS */;
/*!40000 ALTER TABLE `authorisedentry` ENABLE KEYS */;
UNLOCK TABLES;
 
--
-- Table structure for table `edgeconnectors`
--
 
DROP TABLE IF EXISTS `edgeconnectors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `edgeconnectors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `edgename` varchar(45) NOT NULL,
  `ipaddress` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
 
--
-- Dumping data for table `edgeconnectors`
--
 
LOCK TABLES `edgeconnectors` WRITE;
/*!40000 ALTER TABLE `edgeconnectors` DISABLE KEYS */;
INSERT INTO `edgeconnectors` VALUES (1,'Camera','192.168.18.14'),(2,'Camera','192.168.3.3');
/*!40000 ALTER TABLE `edgeconnectors` ENABLE KEYS */;
UNLOCK TABLES;
 
--
-- Table structure for table `edgedata`
--
 
DROP TABLE IF EXISTS `edgedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `edgedata` (
  `edgename` varchar(45) NOT NULL,
  `ipaddress` varchar(45) NOT NULL,
  PRIMARY KEY (`edgename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
 
--
-- Dumping data for table `edgedata`
--
 
LOCK TABLES `edgedata` WRITE;
/*!40000 ALTER TABLE `edgedata` DISABLE KEYS */;
/*!40000 ALTER TABLE `edgedata` ENABLE KEYS */;
UNLOCK TABLES;
 
--
-- Table structure for table `emergency`
--
 
DROP TABLE IF EXISTS `emergency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergency` (
  `id` int NOT NULL AUTO_INCREMENT,
  `edgeconnector` varchar(45) NOT NULL,
  `starttime` datetime NOT NULL,
  `endtime` datetime DEFAULT NULL,
  `globalalarm` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
 
--
-- Dumping data for table `emergency`
--
 
LOCK TABLES `emergency` WRITE;
/*!40000 ALTER TABLE `emergency` DISABLE KEYS */;
/*!40000 ALTER TABLE `emergency` ENABLE KEYS */;
UNLOCK TABLES;
 
--
-- Table structure for table `nodes`
--
 
DROP TABLE IF EXISTS `nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nodes` (
  `nodeid` int NOT NULL,
  `nodename` varchar(50) NOT NULL,
  `edgeconnector` int DEFAULT NULL,
  PRIMARY KEY (`nodeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
 
--
-- Dumping data for table `nodes`
--
 
LOCK TABLES `nodes` WRITE;
/*!40000 ALTER TABLE `nodes` DISABLE KEYS */;
/*!40000 ALTER TABLE `nodes` ENABLE KEYS */;
UNLOCK TABLES;
 
--
-- Table structure for table `sensors`
--
 
DROP TABLE IF EXISTS `sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `edgeconnector` varchar(45) NOT NULL,
  `devicename` int NOT NULL,
  `temp` float NOT NULL,
  `lightlevel` float NOT NULL,
  `sensortime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
 
--
-- Dumping data for table `sensors`
--
 
LOCK TABLES `sensors` WRITE;
/*!40000 ALTER TABLE `sensors` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensors` ENABLE KEYS */;
UNLOCK TABLES;
 
--
-- Table structure for table `unauthentry`
--
 
DROP TABLE IF EXISTS `unauthentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unauthentry` (
  `id` int NOT NULL AUTO_INCREMENT,
  `edgeconnector` int DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `file` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `edgeconnector_idx` (`edgeconnector`),
  CONSTRAINT `edgeconnector` FOREIGN KEY (`edgeconnector`) REFERENCES `edgeconnectors` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
 
--
-- Dumping data for table `unauthentry`
--
 
LOCK TABLES `unauthentry` WRITE;
/*!40000 ALTER TABLE `unauthentry` DISABLE KEYS */;
INSERT INTO `unauthentry` VALUES (3,1,'2021-04-09 15:03:00','20210409095758.h264'),(4,1,'2021-04-09 15:03:01','20210409110316.h264'),(5,1,'2021-04-09 15:03:50','20210409095758.h264'),(6,1,'2021-04-09 15:03:52','20210409110316.h264'),(7,1,'2021-04-09 15:09:12','20210409095758.h264'),(8,1,'2021-04-09 15:09:13','20210409110316.h264'),(9,1,'2021-04-09 15:37:52','20210409095758.h264_.mp4'),(10,1,'2021-04-09 15:38:34','20210409095758.h264_.mp4'),(11,1,'2021-04-09 15:39:35','20210409095758.h264_.mp4'),(12,1,'2021-04-09 15:39:37','20210409110316.h264_.mp4'),(13,1,'2021-04-09 15:39:37','20210409151605.h264_.mp4');
/*!40000 ALTER TABLE `unauthentry` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
 
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
 
-- Dump completed on 2021-04-10 17:22:22