import MySQLdb
from _mysql_exceptions import MySQLError

try:
    conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "", db = "akademik_crawler")
except MySQLError, e:
    print "Oops, cannot connect to database. Error %d: %s" % (e.args[0], e.args[1])
    exit()