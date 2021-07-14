--
-- Create Database Ribbon
--
CREATE DATABASE ribbon;

--
-- Table structure for table `options`
--

DROP TABLE IF EXISTS `options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `options`
(
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` DATETIME NOT NULL,
  `buyer` varchar
(100) NOT NULL,
  `txhash` varchar
(100) NOT NULL,
  `optionToken` varchar
(100) NOT NULL,
  `premium` BIGINT NOT NULL,
  `name` varchar
(100) DEFAULT NULL,
  `sellAmount` BIGINT DEFAULT NULL,
  PRIMARY KEY
(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `skew`
--

use ribbon;
DROP TABLE IF EXISTS `deribit_skew`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deribit_skew`
(
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` TIMESTAMP NOT NULL,
  `strike` BIGINT NOT NULL,
  `venue` varchar(100) DEFAULT NULL,
  `oi` BIGINT DEFAULT NULL,
  PRIMARY KEY
(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `deribit_ribbon_skew`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deribit_ribbon_skew`
(
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` TIMESTAMP NOT NULL,
  `strike` BIGINT NOT NULL,
  `venue` varchar
(100) DEFAULT NULL,
  `oi` BIGINT DEFAULT NULL,
  PRIMARY KEY
(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4;
