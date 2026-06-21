-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: weather_db
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `predicted_weather`
--

DROP TABLE IF EXISTS `predicted_weather`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `predicted_weather` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`,`city`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `predicted_weather`
--

LOCK TABLES `predicted_weather` WRITE;
/*!40000 ALTER TABLE `predicted_weather` DISABLE KEYS */;
INSERT INTO `predicted_weather` VALUES (16,'2026-06-22',30.53,'chennai'),(17,'2026-06-23',30.83,'chennai'),(18,'2026-06-24',31.13,'chennai');
/*!40000 ALTER TABLE `predicted_weather` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weather_data`
--

DROP TABLE IF EXISTS `weather_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weather_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`,`city`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weather_data`
--

LOCK TABLES `weather_data` WRITE;
/*!40000 ALTER TABLE `weather_data` DISABLE KEYS */;
INSERT INTO `weather_data` VALUES (1,'2025-12-31',25.6,'chennai'),(2,'2026-01-01',25.6,'chennai'),(3,'2026-01-02',25.8,'chennai'),(4,'2026-01-03',25.6,'chennai'),(5,'2026-01-04',25.1,'chennai'),(6,'2026-01-05',24.8,'chennai'),(7,'2026-01-15',24.9,'chennai'),(8,'2026-01-16',25.2,'chennai'),(9,'2026-01-17',25,'chennai'),(10,'2026-01-18',24.3,'chennai'),(11,'2026-01-19',24.1,'chennai'),(12,'2026-01-20',23.6,'chennai'),(13,'2026-01-21',23.9,'chennai'),(14,'2026-01-22',24.2,'chennai'),(15,'2026-01-23',25.4,'chennai'),(16,'2026-01-24',25.5,'chennai'),(27,'2026-02-09',25.3,'chennai'),(28,'2026-02-10',25.6,'chennai'),(29,'2026-02-11',25.2,'chennai'),(30,'2026-02-12',25.3,'chennai'),(31,'2026-02-13',25.5,'chennai'),(32,'2026-02-14',25.9,'chennai'),(33,'2026-02-15',25.9,'chennai'),(34,'2026-02-16',25.9,'chennai'),(35,'2026-02-17',25.9,'chennai'),(36,'2026-02-18',25.9,'chennai'),(37,'2026-02-19',25.8,'chennai'),(38,'2026-06-09',33.8,'chennai'),(39,'2026-06-10',33.6,'chennai'),(40,'2026-06-11',30.8,'chennai'),(41,'2026-06-12',30.4,'chennai'),(42,'2026-06-13',30.6,'chennai'),(43,'2026-06-14',31.4,'chennai'),(44,'2026-06-15',31.9,'chennai'),(45,'2026-06-16',32.8,'chennai'),(46,'2026-06-17',32.6,'chennai'),(47,'2026-06-18',31,'chennai'),(48,'2026-06-19',30.4,'chennai'),(58,'2026-06-20',29.9,'chennai'),(59,'2026-06-21',30.4,'chennai');
/*!40000 ALTER TABLE `weather_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-21 18:08:36
