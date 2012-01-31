-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 31, 2012 at 07:07 AM
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
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=953 ;

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

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
