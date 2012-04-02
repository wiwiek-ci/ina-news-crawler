# To change this template, choose Tools | Templates
# and open the template in the editor.

import os
import sys
import time

__author__ = "asatrya"
__date__ = "$May 28, 2011 11:13:42 PM$"

seeder_interval = 60 * 5
fetcher_interval = 1
sites = [
	"detiknews",
	"kompas",
	"mediaindonesia"
]

if len(sys.argv) < 2:
    print "Argument: 'seeder' or 'fetcher'"
    exit()

if sys.argv[1] == "seeder":
    cmd = "scrapy crawl "
    for site in sites:
        cmd += "seeder-" + site + " "
    cmd += " --nolog"
    print "Running Seeder (Press Ctrl+C to stop)"
    is_continue = True
    while is_continue:
        try:
            os.system(cmd)
            time.sleep(seeder_interval)
        except (KeyboardInterrupt, SystemExit):
            is_continue = False
            print "Program will exit..."
elif sys.argv[1] == "fetcher":
    cmd = "scrapy crawl "
    for site in sites:
        cmd += "fetcher-" + site + " "
    cmd += " --nolog"
    print "Running Fetcher (Press Ctrl+C to stop)"
    is_continue = True
    while is_continue:
        try:
			os.system(cmd)
			time.sleep(fetcher_interval)
        except (KeyboardInterrupt, SystemExit):
            is_continue = False
            print "Program will exit..."
elif sys.argv[1] == "fetcher-single":
	cmd = "scrapy crawl "
	cmd += "fetcher-" + sys.argv[2] + " "
	cmd += " --nolog"
	print "Running Fetcher (Press Ctrl+C to stop)"
	is_continue = True
	while is_continue:
		try:
			os.system(cmd)
			time.sleep(fetcher_interval)
		except (KeyboardInterrupt, SystemExit):
			is_continue = False
			print "Program will exit..."
else:
    print "Argument: 'seeder' or 'fetcher'"
    exit()

print "Program exit."