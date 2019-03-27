-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 27, 2019 at 04:44 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `EducEco`
--

-- --------------------------------------------------------

--
-- Table structure for table `HPS`
--

CREATE TABLE `HPS` (
  `id` int(11) NOT NULL,
  `RunID` int(11) UNSIGNED NOT NULL,
  `Timestamp` int(10) UNSIGNED NOT NULL,
  `Speedx10` tinyint(3) UNSIGNED NOT NULL,
  `Pedal` tinyint(3) UNSIGNED NOT NULL,
  `Temp1` tinyint(3) UNSIGNED NOT NULL,
  `Temp2` tinyint(3) UNSIGNED NOT NULL,
  `Temp3` tinyint(3) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `LPS`
--

CREATE TABLE `LPS` (
  `id` int(11) NOT NULL,
  `RunID` int(10) UNSIGNED NOT NULL,
  `Timestamp` int(10) UNSIGNED NOT NULL,
  `Lat` float NOT NULL,
  `Lon` float NOT NULL,
  `SatNbr` tinyint(3) UNSIGNED NOT NULL,
  `Current` tinyint(3) UNSIGNED NOT NULL,
  `Voltage` tinyint(3) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Parameters`
--

CREATE TABLE `Parameters` (
  `id` int(11) NOT NULL,
  `RunID` int(11) NOT NULL,
  `StartTime` datetime NOT NULL,
  `BatteryCap` int(11) NOT NULL,
  `mHPSDelay` int(11) NOT NULL,
  `mLPSDelay` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `HPS`
--
ALTER TABLE `HPS`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `LPS`
--
ALTER TABLE `LPS`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Parameters`
--
ALTER TABLE `Parameters`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `HPS`
--
ALTER TABLE `HPS`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `LPS`
--
ALTER TABLE `LPS`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Parameters`
--
ALTER TABLE `Parameters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
