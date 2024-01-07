CREATE DATABASE  IF NOT EXISTS `device_manager` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `device_manager`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: device_manager
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add site',7,'add_site'),(26,'Can change site',7,'change_site'),(27,'Can delete site',7,'delete_site'),(28,'Can view site',7,'view_site'),(29,'Can add building',8,'add_building'),(30,'Can change building',8,'change_building'),(31,'Can delete building',8,'delete_building'),(32,'Can view building',8,'view_building'),(33,'Can add category',9,'add_category'),(34,'Can change category',9,'change_category'),(35,'Can delete category',9,'delete_category'),(36,'Can view category',9,'view_category'),(37,'Can add floor',10,'add_floor'),(38,'Can change floor',10,'change_floor'),(39,'Can delete floor',10,'delete_floor'),(40,'Can view floor',10,'view_floor'),(41,'Can add room',11,'add_room'),(42,'Can change room',11,'change_room'),(43,'Can delete room',11,'delete_room'),(44,'Can view room',11,'view_room'),(45,'Can add subcategory',12,'add_subcategory'),(46,'Can change subcategory',12,'change_subcategory'),(47,'Can delete subcategory',12,'delete_subcategory'),(48,'Can view subcategory',12,'view_subcategory'),(49,'Can add device',13,'add_device'),(50,'Can change device',13,'change_device'),(51,'Can delete device',13,'delete_device'),(52,'Can view device',13,'view_device');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_bin NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_bin NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$VT1lNAdakd1JNhxK9UyMlZ$jmWKHQFoFvYjLzjizsqmoJrruKLXbXA01/L4NXC5lBM=','2024-01-07 13:52:02.210854',1,'admin','','','admin@django.com',1,1,'2024-01-07 13:51:49.743258');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices_building`
--

DROP TABLE IF EXISTS `devices_building`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices_building` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `address` longtext COLLATE utf8mb4_bin NOT NULL,
  `acronym` varchar(10) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `acronym` (`acronym`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices_building`
--

LOCK TABLES `devices_building` WRITE;
/*!40000 ALTER TABLE `devices_building` DISABLE KEYS */;
INSERT INTO `devices_building` VALUES (1,'Faculty of Electronics Telecommunications and Information Technology Iasi - Body A','Bd. Carol I, no. 11 A, Iaşi, 700506','ETTI'),(2,'Faculty of Electronics Telecommunications and Information Technology Iasi - Body C','Strada Lascăr Catargi 38, Iași 700107','ETTI - C');
/*!40000 ALTER TABLE `devices_building` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices_category`
--

DROP TABLE IF EXISTS `devices_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices_category`
--

LOCK TABLES `devices_category` WRITE;
/*!40000 ALTER TABLE `devices_category` DISABLE KEYS */;
INSERT INTO `devices_category` VALUES (1,'Computers'),(2,'Labware'),(3,'Network'),(4,'Peripherals'),(5,'Storage'),(6,'Other');
/*!40000 ALTER TABLE `devices_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices_device`
--

DROP TABLE IF EXISTS `devices_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices_device` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `serial_number` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `is_qrcode_applied` tinyint(1) NOT NULL,
  `qrcode_url` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `building_id` bigint NOT NULL,
  `category_id` bigint NOT NULL,
  `floor_id` bigint NOT NULL,
  `room_id` bigint NOT NULL,
  `subcategory_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `serial_number` (`serial_number`),
  KEY `devices_device_building_id_b743f4c1_fk_devices_building_id` (`building_id`),
  KEY `devices_device_category_id_bb9413d6_fk_devices_category_id` (`category_id`),
  KEY `devices_device_floor_id_87554dc9_fk_devices_floor_id` (`floor_id`),
  KEY `devices_device_room_id_a7c9b1fc_fk_devices_room_id` (`room_id`),
  KEY `devices_device_subcategory_id_92d6543b_fk_devices_subcategory_id` (`subcategory_id`),
  CONSTRAINT `devices_device_building_id_b743f4c1_fk_devices_building_id` FOREIGN KEY (`building_id`) REFERENCES `devices_building` (`id`),
  CONSTRAINT `devices_device_category_id_bb9413d6_fk_devices_category_id` FOREIGN KEY (`category_id`) REFERENCES `devices_category` (`id`),
  CONSTRAINT `devices_device_floor_id_87554dc9_fk_devices_floor_id` FOREIGN KEY (`floor_id`) REFERENCES `devices_floor` (`id`),
  CONSTRAINT `devices_device_room_id_a7c9b1fc_fk_devices_room_id` FOREIGN KEY (`room_id`) REFERENCES `devices_room` (`id`),
  CONSTRAINT `devices_device_subcategory_id_92d6543b_fk_devices_subcategory_id` FOREIGN KEY (`subcategory_id`) REFERENCES `devices_subcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices_device`
--

LOCK TABLES `devices_device` WRITE;
/*!40000 ALTER TABLE `devices_device` DISABLE KEYS */;
INSERT INTO `devices_device` VALUES (1,'Cisco Server','Description','A1234',0,'/media/qrcodes/1.png','2024-01-07 15:54:42.298324','2024-01-07 15:54:42.298324',1,3,11,1111,33);
/*!40000 ALTER TABLE `devices_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices_floor`
--

DROP TABLE IF EXISTS `devices_floor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices_floor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(5) COLLATE utf8mb4_bin NOT NULL,
  `building_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devices_floor_building_id_ca16fcce_fk_devices_building_id` (`building_id`),
  CONSTRAINT `devices_floor_building_id_ca16fcce_fk_devices_building_id` FOREIGN KEY (`building_id`) REFERENCES `devices_building` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices_floor`
--

LOCK TABLES `devices_floor` WRITE;
/*!40000 ALTER TABLE `devices_floor` DISABLE KEYS */;
INSERT INTO `devices_floor` VALUES (11,'1',1),(12,'2',1),(13,'3',1),(21,'0',2),(22,'1',2);
/*!40000 ALTER TABLE `devices_floor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices_room`
--

DROP TABLE IF EXISTS `devices_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices_room` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(5) COLLATE utf8mb4_bin NOT NULL,
  `building_id` bigint NOT NULL,
  `floor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devices_room_building_id_e98919dd_fk_devices_building_id` (`building_id`),
  KEY `devices_room_floor_id_2525db0d_fk_devices_floor_id` (`floor_id`),
  CONSTRAINT `devices_room_building_id_e98919dd_fk_devices_building_id` FOREIGN KEY (`building_id`) REFERENCES `devices_building` (`id`),
  CONSTRAINT `devices_room_floor_id_2525db0d_fk_devices_floor_id` FOREIGN KEY (`floor_id`) REFERENCES `devices_floor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1339 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices_room`
--

LOCK TABLES `devices_room` WRITE;
/*!40000 ALTER TABLE `devices_room` DISABLE KEYS */;
INSERT INTO `devices_room` VALUES (1108,'1.08',1,11),(1111,'1.11',1,11),(1115,'1.15',1,11),(1203,'2.03',1,12),(1204,'2.04',1,12),(1206,'2.06',1,12),(1208,'2.08',1,12),(1210,'2.10',1,12),(1213,'2.13',1,12),(1223,'2.23',1,12),(1228,'2.28',1,12),(1229,'2.29',1,12),(1307,'3.07',1,13),(1309,'3.09',1,13),(1310,'3.10',1,13),(1312,'3.12',1,13),(1316,'3.16',1,13),(1319,'3.19',1,13),(1322,'3.22',1,13),(1324,'3.24',1,13),(1325,'3.25',1,13),(1326,'3.26',1,13),(1327,'3.27',1,13),(1334,'3.34',1,13),(1337,'3.37',1,13),(1338,'3.38',1,13);
/*!40000 ALTER TABLE `devices_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices_subcategory`
--

DROP TABLE IF EXISTS `devices_subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices_subcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `devices_subcategory_category_id_fe0d675d_fk_devices_category_id` (`category_id`),
  CONSTRAINT `devices_subcategory_category_id_fe0d675d_fk_devices_category_id` FOREIGN KEY (`category_id`) REFERENCES `devices_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices_subcategory`
--

LOCK TABLES `devices_subcategory` WRITE;
/*!40000 ALTER TABLE `devices_subcategory` DISABLE KEYS */;
INSERT INTO `devices_subcategory` VALUES (11,'Laptops',1),(12,'Desktop PCs',1),(21,'Analyzers',2),(22,'Development Boards',2),(23,'Oscilloscopes',2),(24,'Multimeters',2),(25,'Power Supplies',2),(26,'Signal Generators',2),(31,'Routers',3),(32,'Firewalls',3),(33,'Servers',3),(34,'Switches',3),(35,'Racks',3),(41,'Cameras',4),(42,'Microphones',4),(43,'Printers',4),(44,'Projectors',4),(45,'Scanners',4),(51,'Hard Drives',5),(52,'SSDs',5),(53,'NAS',5);
/*!40000 ALTER TABLE `devices_subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_bin,
  `object_repr` varchar(200) COLLATE utf8mb4_bin NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_bin NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'devices','building'),(9,'devices','category'),(13,'devices','device'),(10,'devices','floor'),(11,'devices','room'),(12,'devices','subcategory'),(6,'sessions','session'),(7,'sites','site');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-01-07 13:44:37.117170'),(2,'auth','0001_initial','2024-01-07 13:44:37.833819'),(3,'admin','0001_initial','2024-01-07 13:44:37.998360'),(4,'admin','0002_logentry_remove_auto_add','2024-01-07 13:44:38.008360'),(5,'admin','0003_logentry_add_action_flag_choices','2024-01-07 13:44:38.023389'),(6,'contenttypes','0002_remove_content_type_name','2024-01-07 13:44:38.113920'),(7,'auth','0002_alter_permission_name_max_length','2024-01-07 13:44:38.194541'),(8,'auth','0003_alter_user_email_max_length','2024-01-07 13:44:38.218303'),(9,'auth','0004_alter_user_username_opts','2024-01-07 13:44:38.227176'),(10,'auth','0005_alter_user_last_login_null','2024-01-07 13:44:38.297183'),(11,'auth','0006_require_contenttypes_0002','2024-01-07 13:44:38.300184'),(12,'auth','0007_alter_validators_add_error_messages','2024-01-07 13:44:38.301218'),(13,'auth','0008_alter_user_username_max_length','2024-01-07 13:44:38.376148'),(14,'auth','0009_alter_user_last_name_max_length','2024-01-07 13:44:38.451201'),(15,'auth','0010_alter_group_name_max_length','2024-01-07 13:44:38.476836'),(16,'auth','0011_update_proxy_permissions','2024-01-07 13:44:38.484848'),(17,'auth','0012_alter_user_first_name_max_length','2024-01-07 13:44:38.557443'),(18,'devices','0001_initial','2024-01-07 13:44:39.372363'),(19,'sessions','0001_initial','2024-01-07 13:44:39.417839'),(20,'sites','0001_initial','2024-01-07 13:44:39.443141'),(21,'sites','0002_alter_domain_unique','2024-01-07 13:44:39.460445'),(22,'devices','0002_alter_building_name','2024-01-07 13:53:59.398573');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_bin NOT NULL,
  `session_data` longtext COLLATE utf8mb4_bin NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'device_manager'
--

--
-- Dumping routines for database 'device_manager'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-07 15:59:10
