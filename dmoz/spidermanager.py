from scrapy.spidermanager import SpiderManager

from __init__ import *

class MySpiderManager(SpiderManager):
    def create(self, spider_name, **spider_kwargs):
        global conn
        # Delete in case
        cursor = conn.cursor()
        query = """
            DELETE FROM status
            WHERE spider = %s
        """
        cursor.execute(query, (spider_name))

        # Then insert
        cursor = conn.cursor()
        query = """
            INSERT INTO status(spider, status, lastactive_at)
            VALUES(%s, 1, NOW())
        """
        cursor.execute(query, (spider_name))

        return super(MySpiderManager, self).create(spider_name, **spider_kwargs)

    def close_spider(self, spider, reason):
        global conn
        # Delete in case
        cursor = conn.cursor()
        query = """
            DELETE FROM status
            WHERE spider = %s
        """
        cursor.execute(query, (spider.name))

        # Then insert
        cursor = conn.cursor()
        query = """
            INSERT INTO status(spider, status, lastactive_at)
            VALUES(%s, 0, NOW())
        """
        cursor.execute(query, (spider.name))

        return super(MySpiderManager, self).close_spider(spider, reason)

