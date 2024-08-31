CREATE DATABASE  IF NOT EXISTS `agroforecast_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `agroforecast_db`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: agroforecast_db
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `previsao_dia`
--

DROP TABLE IF EXISTS `previsao_dia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `previsao_dia` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cidade` varchar(255) DEFAULT NULL,
  `data` date DEFAULT NULL,
  `descricao` varchar(255) DEFAULT NULL,
  `temperatura` float DEFAULT NULL,
  `temp_max` float DEFAULT NULL,
  `temp_min` float DEFAULT NULL,
  `sensacao_termica` float DEFAULT NULL,
  `precipitacao` float DEFAULT NULL,
  `umidade` float DEFAULT NULL,
  `qualidade_ar` varchar(255) DEFAULT NULL,
  `co` float DEFAULT NULL,
  `no` float DEFAULT NULL,
  `no2` float DEFAULT NULL,
  `o3` float DEFAULT NULL,
  `so2` float DEFAULT NULL,
  `pm2_5` float DEFAULT NULL,
  `pm10` float DEFAULT NULL,
  `nh3` float DEFAULT NULL,
  `indice_uv` varchar(255) DEFAULT NULL,
  `velocidade_vento` float DEFAULT NULL,
  `visibilidade` float DEFAULT NULL,
  `nebulosidade` float DEFAULT NULL,
  `nascer_sol` time DEFAULT NULL,
  `por_sol` time DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `previsao_dia`
--

LOCK TABLES `previsao_dia` WRITE;
/*!40000 ALTER TABLE `previsao_dia` DISABLE KEYS */;
/*!40000 ALTER TABLE `previsao_dia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `previsoes_futuras`
--

DROP TABLE IF EXISTS `previsoes_futuras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `previsoes_futuras` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cidade` varchar(255) DEFAULT NULL,
  `data_hora` datetime DEFAULT NULL,
  `temperatura` float DEFAULT NULL,
  `sensacao_termica` float DEFAULT NULL,
  `temp_min` float DEFAULT NULL,
  `temp_max` float DEFAULT NULL,
  `pressao` int DEFAULT NULL,
  `umidade` int DEFAULT NULL,
  `descricao` varchar(255) DEFAULT NULL,
  `nuvens` int DEFAULT NULL,
  `velocidade_vento` float DEFAULT NULL,
  `direcao_vento` int DEFAULT NULL,
  `chuva` float DEFAULT NULL,
  `visibilidade` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `previsoes_futuras`
--

LOCK TABLES `previsoes_futuras` WRITE;
/*!40000 ALTER TABLE `previsoes_futuras` DISABLE KEYS */;
/*!40000 ALTER TABLE `previsoes_futuras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `senha` varchar(255) DEFAULT NULL,
  `nome_completo` varchar(255) DEFAULT NULL,
  `genero` varchar(255) DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  `celular` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nacionalidade` varchar(255) DEFAULT NULL,
  `cultura_agricola` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'agroforecast@adm.com','2580','adm','Masculino','1999-08-14','21985367992','2024-06-27 19:25:08','2024-06-27 16:25:08','Brasil'),(2,'douglas@gmail.com','adm','Douglas','Masculino','2024-06-27','21985367992','2024-06-27 21:58:50','Brasil','milho'),(3,'luiz.mendesbarbosa@hotmail.com','adm','Luiz Mendes Barbosa','Masculino','2024-06-28','21985367992','2024-06-28 17:12:14','Brasil','Laraja'),(4,'TESTE@TESTE','TESTE','TESTE TESTE TESTE','Masculino','2024-06-28','TESTE','2024-06-28 17:58:52','TESTE','TESTE'),(5,'franciscoMendes@hotmail.com','2580','Francisco Mendes da Silva Neto','Masculino','2013-04-17','99988283028','2024-06-28 21:47:40','Brasil','Arroz'),(6,'douglas.antonio@hotmail.com','2580','Douglas antonio da silva','Masculino','2024-06-28','21985367992','2024-06-28 23:19:27','Brazil','Repolho'),(7,'carol@hotmail.com','2580','Carol Algustas Marcedo','Masculino','2024-06-29','21985367992','2024-06-29 15:43:41','Rio de Jaeiro','Arroz'),(9,'luizinho.kj@hotmail.com','25802414','Luiz Mendes Barbosa','Masculino','2024-06-29','21985367992','2024-06-29 16:41:23','Brasil','abobora'),(10,'pedro@gmail.com','2580','Pedro','Masculino','2024-06-29','21985367992','2024-06-29 17:34:24','Brasl','laraja'),(12,'amarelo@gmail.com','2580','amarelo henrique sampaio','Masculino','2024-06-30','21985367992','2024-06-30 04:44:34','Paraguai','Limão');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-01 11:11:39
