-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.35 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour cardpresso_db
CREATE DATABASE IF NOT EXISTS `cardpresso_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cardpresso_db`;

-- Listage de la structure de la table cardpresso_db. department
CREATE TABLE IF NOT EXISTS `department` (
  `IDDepartment` int NOT NULL,
  `Name` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`IDDepartment`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table cardpresso_db.department : ~5 rows (environ)
INSERT INTO `department` (`IDDepartment`, `Name`) VALUES
	(1, 'IT'),
	(2, 'HR'),
	(3, 'Production'),
	(4, 'FInance'),
	(5, 'Labo');

-- Listage de la structure de la table cardpresso_db. people
CREATE TABLE IF NOT EXISTS `people` (
  `IDPerson` int NOT NULL,
  `IDCard` int DEFAULT NULL,
  `Lastname` varchar(50) DEFAULT NULL,
  `Firstname` varchar(50) DEFAULT NULL,
  `Site` int DEFAULT NULL,
  `Department` int DEFAULT NULL,
  `IDSAP` bigint DEFAULT NULL,
  PRIMARY KEY (`IDPerson`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table cardpresso_db.people : ~4 rows (environ)
INSERT INTO `people` (`IDPerson`, `IDCard`, `Lastname`, `Firstname`, `Site`, `Department`, `IDSAP`) VALUES
	(1, 3999, 'de_Courville', 'Gaspard', 1, 1, 1000000),
	(2, 4000, 'Loiseau', 'Marc', 1, 2, 1000001),
	(3, 4001, 'Perrier', 'Walser', 2, 1, 1000002),
	(4, 4002, 'Rocher', 'Pierre', 3, 4, 1000003);

-- Listage de la structure de la table cardpresso_db. site
CREATE TABLE IF NOT EXISTS `site` (
  `IDSite` int NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`IDSite`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table cardpresso_db.site : ~3 rows (environ)
INSERT INTO `site` (`IDSite`, `Name`) VALUES
	(1, 'Eclépens'),
	(2, 'Säffle'),
	(3, 'USA');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
