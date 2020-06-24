-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  mer. 24 juin 2020 à 10:07
-- Version du serveur :  10.4.10-MariaDB
-- Version de PHP :  7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `educeco`
--

-- --------------------------------------------------------

--
-- Structure de la table `acceleratorposition`
--

DROP TABLE IF EXISTS `acceleratorposition`;
CREATE TABLE IF NOT EXISTS `acceleratorposition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Position` int(11) NOT NULL,
  `TS` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `battery`
--

DROP TABLE IF EXISTS `battery`;
CREATE TABLE IF NOT EXISTS `battery` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Cell1` float NOT NULL,
  `Cell2` float NOT NULL,
  `Cell3` float NOT NULL,
  `TS` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `current`
--

DROP TABLE IF EXISTS `current`;
CREATE TABLE IF NOT EXISTS `current` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Current` float NOT NULL,
  `TS` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `logs`
--

DROP TABLE IF EXISTS `logs`;
CREATE TABLE IF NOT EXISTS `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Process` varchar(10) NOT NULL,
  `TYPE` varchar(10) NOT NULL,
  `Message` text NOT NULL,
  `TS` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `pautonomy`
--

DROP TABLE IF EXISTS `pautonomy`;
CREATE TABLE IF NOT EXISTS `pautonomy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Time` int(11) NOT NULL,
  `TS` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `pbattery`
--

DROP TABLE IF EXISTS `pbattery`;
CREATE TABLE IF NOT EXISTS `pbattery` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Percentage` int(11) NOT NULL,
  `TS` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `pdistance`
--

DROP TABLE IF EXISTS `pdistance`;
CREATE TABLE IF NOT EXISTS `pdistance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Distance` float NOT NULL,
  `TS` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `pinstantpower`
--

DROP TABLE IF EXISTS `pinstantpower`;
CREATE TABLE IF NOT EXISTS `pinstantpower` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Power` float NOT NULL,
  `TS` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `speed`
--

DROP TABLE IF EXISTS `speed`;
CREATE TABLE IF NOT EXISTS `speed` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Speed` float NOT NULL,
  `TS` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `temperature`
--

DROP TABLE IF EXISTS `temperature`;
CREATE TABLE IF NOT EXISTS `temperature` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Temp1` float NOT NULL,
  `Temp2` float NOT NULL,
  `Temp3` float NOT NULL,
  `TS` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
