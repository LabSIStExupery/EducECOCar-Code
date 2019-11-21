-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le :  jeu. 21 nov. 2019 à 22:41
-- Version du serveur :  10.2.24-MariaDB-10.2.24+maria~stretch-log
-- Version de PHP :  7.0.33-8+0~20190531121058.14+stretch~1.gbpe7d4ff

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `Educeco`
--

-- --------------------------------------------------------

--
-- Structure de la table `AcceleratorPosition`
--

CREATE TABLE `AcceleratorPosition` (
  `id` int(11) NOT NULL,
  `Position` int(11) NOT NULL,
  `TIMESTAMP` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Battery`
--

CREATE TABLE `Battery` (
  `id` int(11) NOT NULL,
  `Cell1` float NOT NULL,
  `Cell2` float NOT NULL,
  `Cell3` float NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Current`
--

CREATE TABLE `Current` (
  `id` int(11) NOT NULL,
  `Current` float NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Logs`
--

CREATE TABLE `Logs` (
  `id` int(11) NOT NULL,
  `Process` varchar(10) NOT NULL,
  `TYPE` varchar(10) NOT NULL,
  `Message` text NOT NULL,
  `TIMESTAMP` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `PAutonomy`
--

CREATE TABLE `PAutonomy` (
  `id` int(11) NOT NULL,
  `Time` int(11) NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `PBattery`
--

CREATE TABLE `PBattery` (
  `id` int(11) NOT NULL,
  `Percentage` int(11) NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `PDistance`
--

CREATE TABLE `PDistance` (
  `id` int(11) NOT NULL,
  `Distance` float NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `PInstantPower`
--

CREATE TABLE `PInstantPower` (
  `id` int(11) NOT NULL,
  `Power` float NOT NULL,
  `TIMESTAMP` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Speed`
--

CREATE TABLE `Speed` (
  `id` int(11) NOT NULL,
  `Speed` float NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `Temperature`
--

CREATE TABLE `Temperature` (
  `id` int(11) NOT NULL,
  `Temp1` float NOT NULL,
  `Temp2` float NOT NULL,
  `Temp3` float NOT NULL,
  `TIMESTAMP` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `AcceleratorPosition`
--
ALTER TABLE `AcceleratorPosition`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `Battery`
--
ALTER TABLE `Battery`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `Current`
--
ALTER TABLE `Current`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `Logs`
--
ALTER TABLE `Logs`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Index pour la table `PAutonomy`
--
ALTER TABLE `PAutonomy`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `PBattery`
--
ALTER TABLE `PBattery`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `PDistance`
--
ALTER TABLE `PDistance`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `PInstantPower`
--
ALTER TABLE `PInstantPower`
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
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `AcceleratorPosition`
--
ALTER TABLE `AcceleratorPosition`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Battery`
--
ALTER TABLE `Battery`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Current`
--
ALTER TABLE `Current`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Logs`
--
ALTER TABLE `Logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `PAutonomy`
--
ALTER TABLE `PAutonomy`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `PBattery`
--
ALTER TABLE `PBattery`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `PDistance`
--
ALTER TABLE `PDistance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `PInstantPower`
--
ALTER TABLE `PInstantPower`
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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
