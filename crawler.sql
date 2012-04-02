-- phpMyAdmin SQL Dump
-- version 3.4.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 02, 2012 at 08:52 AM
-- Server version: 5.5.16
-- PHP Version: 5.3.8

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `akademik_crawler`
--

-- --------------------------------------------------------

--
-- Table structure for table `article`
--

CREATE TABLE IF NOT EXISTS `article` (
  `id` bigint(20) NOT NULL,
  `source` varchar(25) NOT NULL,
  `url` varchar(500) NOT NULL,
  `category` varchar(25) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `subtitle` varchar(200) DEFAULT NULL,
  `published_at` datetime DEFAULT NULL,
  `place` varchar(25) DEFAULT NULL,
  `author` varchar(25) DEFAULT NULL,
  `is_gathered` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `seed`
--

CREATE TABLE IF NOT EXISTS `seed` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(25) NOT NULL,
  `category` varchar(25) NOT NULL,
  `url` varchar(500) NOT NULL,
  `inserted_by` varchar(25) NOT NULL,
  `inserted_at` datetime NOT NULL,
  `fetched_by` varchar(25) DEFAULT NULL,
  `fetched_at` datetime DEFAULT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'new',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1319 ;

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

CREATE TABLE IF NOT EXISTS `status` (
  `spider` varchar(25) NOT NULL,
  `status` tinyint(4) NOT NULL,
  `lastactive_at` datetime NOT NULL,
  PRIMARY KEY (`spider`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_stats_seed_category`
--
CREATE TABLE IF NOT EXISTS `v_stats_seed_category` (
`source` varchar(25)
,`category` varchar(25)
,`total` bigint(21)
,`new` bigint(21)
,`ok` bigint(21)
,`err` bigint(21)
);
-- --------------------------------------------------------

--
-- Stand-in structure for view `v_stats_seed_date`
--
CREATE TABLE IF NOT EXISTS `v_stats_seed_date` (
`source` varchar(25)
,`insert_date` date
,`total` bigint(21)
,`new` bigint(21)
,`ok` bigint(21)
,`err` bigint(21)
);
-- --------------------------------------------------------

--
-- Stand-in structure for view `v_stats_seed_overall`
--
CREATE TABLE IF NOT EXISTS `v_stats_seed_overall` (
`source` varchar(25)
,`total` bigint(21)
,`new` bigint(21)
,`ok` bigint(21)
,`err` bigint(21)
);
-- --------------------------------------------------------

--
-- Structure for view `v_stats_seed_category`
--
DROP TABLE IF EXISTS `v_stats_seed_category`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_stats_seed_category` AS select `seed`.`source` AS `source`,`seed`.`category` AS `category`,count(`seed`.`id`) AS `total`,count((case when (`seed`.`status` = 'new') then `seed`.`id` end)) AS `new`,count((case when (`seed`.`status` = 'ok') then `seed`.`id` end)) AS `ok`,count((case when (`seed`.`status` = 'err') then `seed`.`id` end)) AS `err` from `seed` group by `seed`.`source`,`seed`.`category`;

-- --------------------------------------------------------

--
-- Structure for view `v_stats_seed_date`
--
DROP TABLE IF EXISTS `v_stats_seed_date`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_stats_seed_date` AS select `seed`.`source` AS `source`,cast(`seed`.`inserted_at` as date) AS `insert_date`,count(`seed`.`id`) AS `total`,count((case when (`seed`.`status` = 'new') then `seed`.`id` end)) AS `new`,count((case when (`seed`.`status` = 'ok') then `seed`.`id` end)) AS `ok`,count((case when (`seed`.`status` = 'err') then `seed`.`id` end)) AS `err` from `seed` group by `seed`.`source`,cast(`seed`.`inserted_at` as date) order by `seed`.`source`,cast(`seed`.`inserted_at` as date);

-- --------------------------------------------------------

--
-- Structure for view `v_stats_seed_overall`
--
DROP TABLE IF EXISTS `v_stats_seed_overall`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_stats_seed_overall` AS select `seed`.`source` AS `source`,count(`seed`.`id`) AS `total`,count((case when (`seed`.`status` = 'new') then `seed`.`id` end)) AS `new`,count((case when (`seed`.`status` = 'ok') then `seed`.`id` end)) AS `ok`,count((case when (`seed`.`status` = 'err') then `seed`.`id` end)) AS `err` from `seed` group by `seed`.`source`;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
