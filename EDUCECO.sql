-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le :  mer. 25 sep. 2019 à 15:28
-- Version du serveur :  10.3.17-MariaDB-0+deb10u1
-- Version de PHP :  7.0.33-0+deb9u3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `EDUCECO`
--

-- --------------------------------------------------------

--
-- Structure de la table `Intensity`
--

CREATE TABLE `Intensity` (
  `id` int(11) NOT NULL,
  `Value` int(11) NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `Speed`
--

CREATE TABLE `Speed` (
  `id` int(11) NOT NULL,
  `Speed` decimal(3,2) NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `Temperature`
--

CREATE TABLE `Temperature` (
  `id` int(11) NOT NULL,
  `SensorIndex` int(1) NOT NULL,
  `Value` decimal(3,2) NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `Voltage`
--

CREATE TABLE `Voltage` (
  `id` int(11) NOT NULL,
  `Cell1` int(11) NOT NULL,
  `Cell2` int(11) NOT NULL,
  `Cell3` int(11) NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Intensity`
--
ALTER TABLE `Intensity`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `Speed`
--
ALTER TABLE `Speed`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `Temperature`
--
ALTER TABLE `Temperature`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `Voltage`
--
ALTER TABLE `Voltage`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Intensity`
--
ALTER TABLE `Intensity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Speed`
--
ALTER TABLE `Speed`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Temperature`
--
ALTER TABLE `Temperature`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Voltage`
--
ALTER TABLE `Voltage`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
