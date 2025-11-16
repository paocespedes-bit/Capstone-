-- MySQL dump 10.13  Distrib 8.4.7, for Win64 (x86_64)
--
-- Host: localhost    Database: SIPstoreDB
-- ------------------------------------------------------
-- Server version	8.4.7

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
-- Table structure for table `accounts_customuser`
--

DROP TABLE IF EXISTS `accounts_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `celular` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `correo_de_respaldo` varchar(254) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo_usuario` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `correo_de_respaldo` (`correo_de_respaldo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser`
--

LOCK TABLES `accounts_customuser` WRITE;
/*!40000 ALTER TABLE `accounts_customuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_groups`
--

DROP TABLE IF EXISTS `accounts_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq` (`customuser_id`,`group_id`),
  KEY `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_customuser__customuser_id_bc55088e_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_groups`
--

LOCK TABLES `accounts_customuser_groups` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_user_permissions`
--

DROP TABLE IF EXISTS `accounts_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_user_customuser_id_permission_9632a709_uniq` (`customuser_id`,`permission_id`),
  KEY `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_customuser__customuser_id_0deaefae_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_user_permissions`
--

LOCK TABLES `accounts_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add categoria',6,'add_categoria'),(22,'Can change categoria',6,'change_categoria'),(23,'Can delete categoria',6,'delete_categoria'),(24,'Can view categoria',6,'view_categoria'),(25,'Can add comentario',7,'add_comentario'),(26,'Can change comentario',7,'change_comentario'),(27,'Can delete comentario',7,'delete_comentario'),(28,'Can view comentario',7,'view_comentario'),(29,'Can add imagen producto',8,'add_imagenproducto'),(30,'Can change imagen producto',8,'change_imagenproducto'),(31,'Can delete imagen producto',8,'delete_imagenproducto'),(32,'Can view imagen producto',8,'view_imagenproducto'),(33,'Can add inventario',9,'add_inventario'),(34,'Can change inventario',9,'change_inventario'),(35,'Can delete inventario',9,'delete_inventario'),(36,'Can view inventario',9,'view_inventario'),(37,'Can add kit construccion',10,'add_kitconstruccion'),(38,'Can change kit construccion',10,'change_kitconstruccion'),(39,'Can delete kit construccion',10,'delete_kitconstruccion'),(40,'Can view kit construccion',10,'view_kitconstruccion'),(41,'Can add oferta',11,'add_oferta'),(42,'Can change oferta',11,'change_oferta'),(43,'Can delete oferta',11,'delete_oferta'),(44,'Can view oferta',11,'view_oferta'),(45,'Can add panel sip',12,'add_panelsip'),(46,'Can change panel sip',12,'change_panelsip'),(47,'Can delete panel sip',12,'delete_panelsip'),(48,'Can view panel sip',12,'view_panelsip'),(49,'Can add local',13,'add_local'),(50,'Can change local',13,'change_local'),(51,'Can delete local',13,'delete_local'),(52,'Can view local',13,'view_local'),(53,'Can add pedido',14,'add_pedido'),(54,'Can change pedido',14,'change_pedido'),(55,'Can delete pedido',14,'delete_pedido'),(56,'Can view pedido',14,'view_pedido'),(57,'Can add detalle pedido',15,'add_detallepedido'),(58,'Can change detalle pedido',15,'change_detallepedido'),(59,'Can delete detalle pedido',15,'delete_detallepedido'),(60,'Can view detalle pedido',15,'view_detallepedido'),(61,'Can add Usuario Personalizado',16,'add_customuser'),(62,'Can change Usuario Personalizado',16,'change_customuser'),(63,'Can delete Usuario Personalizado',16,'delete_customuser'),(64,'Can view Usuario Personalizado',16,'view_customuser'),(65,'Can add calificacion',17,'add_calificacion'),(66,'Can change calificacion',17,'change_calificacion'),(67,'Can delete calificacion',17,'delete_calificacion'),(68,'Can view calificacion',17,'view_calificacion');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coment_calificacion`
--

DROP TABLE IF EXISTS `coment_calificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coment_calificacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned NOT NULL,
  `estrellas` int unsigned NOT NULL,
  `comentario` longtext COLLATE utf8mb4_general_ci,
  `fecha` datetime(6) NOT NULL,
  `content_type_id` int NOT NULL,
  `usuario_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `coment_calificacion_usuario_id_content_type__15a07e97_uniq` (`usuario_id`,`content_type_id`,`object_id`),
  KEY `coment_calificacion_content_type_id_dc699235_fk_django_co` (`content_type_id`),
  CONSTRAINT `coment_calificacion_content_type_id_dc699235_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `coment_calificacion_usuario_id_2aab6e4c_fk_accounts_` FOREIGN KEY (`usuario_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `coment_calificacion_chk_1` CHECK ((`object_id` >= 0)),
  CONSTRAINT `coment_calificacion_chk_2` CHECK ((`estrellas` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coment_calificacion`
--

LOCK TABLES `coment_calificacion` WRITE;
/*!40000 ALTER TABLE `coment_calificacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `coment_calificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_detallepedido`
--

DROP TABLE IF EXISTS `control_detallepedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `control_detallepedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned DEFAULT NULL,
  `nombre_producto` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `cantidad` int unsigned NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `pedido_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `control_detallepedid_content_type_id_4041bdb6_fk_django_co` (`content_type_id`),
  KEY `control_detallepedido_pedido_id_f024e265_fk_control_pedido_id` (`pedido_id`),
  CONSTRAINT `control_detallepedid_content_type_id_4041bdb6_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `control_detallepedido_pedido_id_f024e265_fk_control_pedido_id` FOREIGN KEY (`pedido_id`) REFERENCES `control_pedido` (`id`),
  CONSTRAINT `control_detallepedido_chk_1` CHECK ((`object_id` >= 0)),
  CONSTRAINT `control_detallepedido_chk_2` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_detallepedido`
--

LOCK TABLES `control_detallepedido` WRITE;
/*!40000 ALTER TABLE `control_detallepedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_detallepedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_local`
--

DROP TABLE IF EXISTS `control_local`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `control_local` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `ubicacion` varchar(300) COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_local`
--

LOCK TABLES `control_local` WRITE;
/*!40000 ALTER TABLE `control_local` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_local` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_pedido`
--

DROP TABLE IF EXISTS `control_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `control_pedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_local` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `comprador` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `rut_cli` varchar(12) COLLATE utf8mb4_general_ci NOT NULL,
  `correo_cli` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `celular_cli` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `ubicacion_cli` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_pedido` datetime(6) NOT NULL,
  `fecha_retiro` datetime(6) DEFAULT NULL,
  `estado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `monto_total` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `local_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `control_pedido_local_id_b6bbbb58_fk_control_local_id` (`local_id`),
  CONSTRAINT `control_pedido_local_id_b6bbbb58_fk_control_local_id` FOREIGN KEY (`local_id`) REFERENCES `control_local` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_pedido`
--

LOCK TABLES `control_pedido` WRITE;
/*!40000 ALTER TABLE `control_pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_pedido` ENABLE KEYS */;
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
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (16,'accounts','customuser'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(17,'coment','calificacion'),(4,'contenttypes','contenttype'),(15,'control','detallepedido'),(13,'control','local'),(14,'control','pedido'),(5,'sessions','session'),(6,'store','categoria'),(7,'store','comentario'),(8,'store','imagenproducto'),(9,'store','inventario'),(10,'store','kitconstruccion'),(11,'store','oferta'),(12,'store','panelsip');
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
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-11-16 17:33:55.241592'),(2,'contenttypes','0002_remove_content_type_name','2025-11-16 17:33:55.306684'),(3,'auth','0001_initial','2025-11-16 17:33:55.522677'),(4,'auth','0002_alter_permission_name_max_length','2025-11-16 17:33:55.566827'),(5,'auth','0003_alter_user_email_max_length','2025-11-16 17:33:55.571006'),(6,'auth','0004_alter_user_username_opts','2025-11-16 17:33:55.574365'),(7,'auth','0005_alter_user_last_login_null','2025-11-16 17:33:55.577649'),(8,'auth','0006_require_contenttypes_0002','2025-11-16 17:33:55.578743'),(9,'auth','0007_alter_validators_add_error_messages','2025-11-16 17:33:55.582110'),(10,'auth','0008_alter_user_username_max_length','2025-11-16 17:33:55.585866'),(11,'auth','0009_alter_user_last_name_max_length','2025-11-16 17:33:55.589619'),(12,'auth','0010_alter_group_name_max_length','2025-11-16 17:33:55.597946'),(13,'auth','0011_update_proxy_permissions','2025-11-16 17:33:55.601660'),(14,'auth','0012_alter_user_first_name_max_length','2025-11-16 17:33:55.604915'),(15,'accounts','0001_initial','2025-11-16 17:33:55.782028'),(16,'admin','0001_initial','2025-11-16 17:33:55.862930'),(17,'admin','0002_logentry_remove_auto_add','2025-11-16 17:33:55.869013'),(18,'admin','0003_logentry_add_action_flag_choices','2025-11-16 17:33:55.874329'),(19,'coment','0001_initial','2025-11-16 17:33:55.985666'),(20,'control','0001_initial','2025-11-16 17:33:56.133185'),(21,'sessions','0001_initial','2025-11-16 17:33:56.158058'),(22,'store','0001_initial','2025-11-16 17:33:56.568182');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_categoria`
--

DROP TABLE IF EXISTS `store_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_categoria`
--

LOCK TABLES `store_categoria` WRITE;
/*!40000 ALTER TABLE `store_categoria` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_comentario`
--

DROP TABLE IF EXISTS `store_comentario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_comentario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned NOT NULL,
  `autor` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `texto` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_comentario` time(6) NOT NULL,
  `estrellas` decimal(3,1) NOT NULL,
  `content_type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_comentario_content_type_id_df3940f3_fk_django_co` (`content_type_id`),
  CONSTRAINT `store_comentario_content_type_id_df3940f3_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `store_comentario_chk_1` CHECK ((`object_id` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_comentario`
--

LOCK TABLES `store_comentario` WRITE;
/*!40000 ALTER TABLE `store_comentario` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_comentario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_imagenproducto`
--

DROP TABLE IF EXISTS `store_imagenproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_imagenproducto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned NOT NULL,
  `imagen` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_imagenproducto_content_type_id_a9b273e7_fk_django_co` (`content_type_id`),
  CONSTRAINT `store_imagenproducto_content_type_id_a9b273e7_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `store_imagenproducto_chk_1` CHECK ((`object_id` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_imagenproducto`
--

LOCK TABLES `store_imagenproducto` WRITE;
/*!40000 ALTER TABLE `store_imagenproducto` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_imagenproducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_inventario`
--

DROP TABLE IF EXISTS `store_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_inventario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned NOT NULL,
  `disponible` int unsigned NOT NULL,
  `reservado` int unsigned NOT NULL,
  `modo_stock` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_inventario_content_type_id_b1882070_fk_django_co` (`content_type_id`),
  CONSTRAINT `store_inventario_content_type_id_b1882070_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `store_inventario_chk_1` CHECK ((`object_id` >= 0)),
  CONSTRAINT `store_inventario_chk_2` CHECK ((`disponible` >= 0)),
  CONSTRAINT `store_inventario_chk_3` CHECK ((`reservado` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_inventario`
--

LOCK TABLES `store_inventario` WRITE;
/*!40000 ALTER TABLE `store_inventario` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_kitconstruccion`
--

DROP TABLE IF EXISTS `store_kitconstruccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_kitconstruccion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `precio` double NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_general_ci,
  `m2` decimal(8,2) NOT NULL,
  `dormitorios` int unsigned NOT NULL,
  `banos` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `store_kitconstruccion_chk_1` CHECK ((`dormitorios` >= 0)),
  CONSTRAINT `store_kitconstruccion_chk_2` CHECK ((`banos` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_kitconstruccion`
--

LOCK TABLES `store_kitconstruccion` WRITE;
/*!40000 ALTER TABLE `store_kitconstruccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_kitconstruccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_kitconstruccion_categorias`
--

DROP TABLE IF EXISTS `store_kitconstruccion_categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_kitconstruccion_categorias` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `kitconstruccion_id` bigint NOT NULL,
  `categoria_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_kitconstruccion_ca_kitconstruccion_id_categ_05e44da0_uniq` (`kitconstruccion_id`,`categoria_id`),
  KEY `store_kitconstruccio_categoria_id_9f8c53ef_fk_store_cat` (`categoria_id`),
  CONSTRAINT `store_kitconstruccio_categoria_id_9f8c53ef_fk_store_cat` FOREIGN KEY (`categoria_id`) REFERENCES `store_categoria` (`id`),
  CONSTRAINT `store_kitconstruccio_kitconstruccion_id_e7e42406_fk_store_kit` FOREIGN KEY (`kitconstruccion_id`) REFERENCES `store_kitconstruccion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_kitconstruccion_categorias`
--

LOCK TABLES `store_kitconstruccion_categorias` WRITE;
/*!40000 ALTER TABLE `store_kitconstruccion_categorias` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_kitconstruccion_categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_oferta`
--

DROP TABLE IF EXISTS `store_oferta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_oferta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned NOT NULL,
  `precio_oferta` double NOT NULL,
  `porcentaje_dcto` int unsigned DEFAULT NULL,
  `fecha_inicio` datetime(6) DEFAULT NULL,
  `fecha_fin` datetime(6) DEFAULT NULL,
  `content_type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_oferta_content_type_id_030bf441_fk_django_content_type_id` (`content_type_id`),
  CONSTRAINT `store_oferta_content_type_id_030bf441_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `store_oferta_chk_1` CHECK ((`object_id` >= 0)),
  CONSTRAINT `store_oferta_chk_2` CHECK ((`porcentaje_dcto` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_oferta`
--

LOCK TABLES `store_oferta` WRITE;
/*!40000 ALTER TABLE `store_oferta` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_oferta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_panelsip`
--

DROP TABLE IF EXISTS `store_panelsip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_panelsip` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `precio` double NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_general_ci,
  `tipo_obs` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `madera_union` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `espesor` decimal(5,2) NOT NULL,
  `largo` decimal(7,2) NOT NULL,
  `ancho` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_panelsip`
--

LOCK TABLES `store_panelsip` WRITE;
/*!40000 ALTER TABLE `store_panelsip` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_panelsip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_panelsip_categorias`
--

DROP TABLE IF EXISTS `store_panelsip_categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_panelsip_categorias` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `panelsip_id` bigint NOT NULL,
  `categoria_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_panelsip_categorias_panelsip_id_categoria_id_f1679d84_uniq` (`panelsip_id`,`categoria_id`),
  KEY `store_panelsip_categ_categoria_id_ef3f20b0_fk_store_cat` (`categoria_id`),
  CONSTRAINT `store_panelsip_categ_categoria_id_ef3f20b0_fk_store_cat` FOREIGN KEY (`categoria_id`) REFERENCES `store_categoria` (`id`),
  CONSTRAINT `store_panelsip_categ_panelsip_id_eb93584c_fk_store_pan` FOREIGN KEY (`panelsip_id`) REFERENCES `store_panelsip` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_panelsip_categorias`
--

LOCK TABLES `store_panelsip_categorias` WRITE;
/*!40000 ALTER TABLE `store_panelsip_categorias` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_panelsip_categorias` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-16 15:01:27
