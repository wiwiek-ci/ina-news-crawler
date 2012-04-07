-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 07, 2012 at 11:59 AM
-- Server version: 5.1.41
-- PHP Version: 5.3.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `source` varchar(25) NOT NULL,
  `url` varchar(500) NOT NULL,
  `category` varchar(25) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `subtitle` varchar(200) DEFAULT NULL,
  `published_at` datetime DEFAULT NULL,
  `place` varchar(25) DEFAULT NULL,
  `author` varchar(25) DEFAULT NULL,
  `fetched_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=49314 ;

-- --------------------------------------------------------

--
-- Table structure for table `v_stats_category`
--

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `akademik_crawler`.`v_stats_category` AS select `akademik_crawler`.`article`.`category` AS `category`,`akademik_crawler`.`article`.`source` AS `source`,count(`akademik_crawler`.`article`.`id`) AS `total` from `akademik_crawler`.`article` group by `akademik_crawler`.`article`.`source`,`akademik_crawler`.`article`.`category` order by `akademik_crawler`.`article`.`category`,`akademik_crawler`.`article`.`source`;

-- --------------------------------------------------------

--
-- Table structure for table `v_stats_date`
--

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `akademik_crawler`.`v_stats_date` AS select `akademik_crawler`.`article`.`source` AS `source`,cast(`akademik_crawler`.`article`.`fetched_at` as date) AS `fetch_date`,count(`akademik_crawler`.`article`.`id`) AS `total` from `akademik_crawler`.`article` group by cast(`akademik_crawler`.`article`.`fetched_at` as date),`akademik_crawler`.`article`.`source` order by `akademik_crawler`.`article`.`source`,cast(`akademik_crawler`.`article`.`fetched_at` as date) desc;

-- --------------------------------------------------------

--
-- Table structure for table `v_stats_source`
--

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `akademik_crawler`.`v_stats_source` AS select `akademik_crawler`.`article`.`source` AS `source`,count(`akademik_crawler`.`article`.`id`) AS `total` from `akademik_crawler`.`article` group by `akademik_crawler`.`article`.`source`;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
