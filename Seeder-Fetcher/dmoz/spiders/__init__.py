# This package will contain the spiders of your Scrapy project
#
# To create the first spider for your project use this command:
#
#   scrapy genspider myspider myspider-domain.com
#
# For more info see:
# http://doc.scrapy.org/topics/spiders.html

import MySQLdb
import re
from _mysql_exceptions import MySQLError

try:
    conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "", db = "akademik_crawler")
except MySQLError, e:
    print "Oops, cannot connect to database. Error %d: %s" % (e.args[0], e.args[1])
    exit()

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def removeHtmlTags(s): return re.sub('<[^<^>]*>', '', s)

def capitalizeFirstCharInWord(s):
    is_find_space = False
    upper_str = s.upper()
    lower_str = s.lower()
    retval = ""
    for i in range(len(s)):
        if i == 0:
            retval += upper_str[i]
        elif s[i] == ' ':
            is_find_space = True
            retval += ' '
        elif is_find_space:
            retval += upper_str[i]
            is_find_space = False
        else:
            retval += lower_str[i]
    return retval

def sanitize(s): return removeHtmlTags(removeNonAscii(s)).strip('- \n\t\s')
