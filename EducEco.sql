-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Mer 27 Mars 2019 à 19:17
-- Version du serveur :  5.7.9
-- Version de PHP :  5.6.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
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
-- Structure de la table `hps`
--

DROP TABLE IF EXISTS `hps`;
CREATE TABLE IF NOT EXISTS `hps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RunID` int(11) UNSIGNED NOT NULL,
  `Timestamp` int(10) UNSIGNED NOT NULL,
  `Speedx10` tinyint(3) UNSIGNED NOT NULL,
  `Pedal` tinyint(3) UNSIGNED NOT NULL,
  `Temp1` tinyint(3) UNSIGNED NOT NULL,
  `Temp2` tinyint(3) UNSIGNED NOT NULL,
  `Temp3` tinyint(3) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `lps`
--

DROP TABLE IF EXISTS `lps`;
CREATE TABLE IF NOT EXISTS `lps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RunID` int(10) UNSIGNED NOT NULL,
  `Timestamp` int(10) UNSIGNED NOT NULL,
  `Lat` float NOT NULL,
  `Lon` float NOT NULL,
  `SatNbr` tinyint(3) UNSIGNED NOT NULL,
  `Current` tinyint(3) UNSIGNED NOT NULL,
  `Voltage` tinyint(3) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `parameters`
--

DROP TABLE IF EXISTS `parameters`;
CREATE TABLE IF NOT EXISTS `parameters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RunID` int(11) NOT NULL,
  `StartTime` datetime NOT NULL,
  `BatteryCap` int(11) NOT NULL,
  `mHPSDelay` int(11) NOT NULL,
  `mLPSDelay` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `runs`
--

DROP TABLE IF EXISTS `runs`;
CREATE TABLE IF NOT EXISTS `runs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `SoftwareVersion` varchar(10) NOT NULL,
  `Driver` varchar(18) NOT NULL,
  `Comment` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
