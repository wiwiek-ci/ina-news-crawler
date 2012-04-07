from scrapy.spidermanager import SpiderManager

from __init__ import *

class MySpiderManager(SpiderManager):
    def create(self, spider_name, **spider_kwargs):
        global conn
        return super(MySpiderManager, self).create(spider_name, **spider_kwargs)

    def close_spider(self, spider, reason):
        global conn
        return super(MySpiderManager, self).close_spider(spider, reason)

