This page explains how to install and run ina-news-crawler program.

# Seeder-Fetcher #
## Installation ##

System requiements:
  * Scrappy. Follow this tutorial: http://doc.scrapy.org/en/latest/intro/install.html
  * MySQL database server

Steps to install:
  * Check out ina-news-crawler code from this repository
  * Create database and modify your database settings at init.py file on base\_directory/dmoz directory
  * Import newscrawler.sql in your installation directory to your database
  * Add project base directory to PYTHONPATH environment variable
  * Add `dmoz.settings` to SCRAPY\_SETTINGS\_MODULE environment variable
  * Download and install MySQL-Python (http://www.codegood.com/archives/129)
  * Download and install Feedparser module (http://code.google.com/p/feedparser/)


## Setup Sites ##

This installation copy is pre-configured with 3 default target sites:
  * detiknews
  * kompas
  * mediaindonesia

To setup custom crawler, follow the Developer Guide.


## Run ##

Steps to run this application:
  * Make sure that Scrapy is listed in your environment path
  * In command line, go to base\_directory directory
  * Run command "scrapy crawl [detiknews/kompas/mediaindonesia/custom-crawler] --nolog" to fetch articles from corresponding site.

# Gatherer #
## Installation ##
System requiements:
  * Java 6
  * GATE 6.0 (http://gate.ac.uk/download/)

Steps to install (build):
  * Check out ina-news-crawler code from this repository
  * Build Gatherer project (in Netbeans project format)
  * Configure GATE plugins and config file path in "run.bat" file
  * Configure database settings and destination folder path in "gatherer.conf" file

## Run ##
Execute run.bat