# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from datetime import datetime
import json
from scrapy.exceptions import DropItem

from __init__ import *

class FilterAndFlagPipeline(object):
    def process_item(self, item, spider):
        global conn

        if len(item['title']) > 0 and len(item['content']) > 0:
            status = "ok"
        else:
            status = "err"
        
        # Print to screen
        # print "[%s] %s Fetch %s: %s" % (spider.name, datetime.now(), item['source'], status)

        if status == "ok":
            return item
        else:
            print "[%s] %s %s (%s)" % (spider.name, datetime.now(), status, item['url'])
            raise DropItem("Drop false article: %s" % item['source'])

class DuplicatePipeline(object):
    def process_item(self, item, spider):
        global conn

        cursor = conn.cursor()
        query = """
            SELECT url
            FROM article
            WHERE url = %s
        """
        cursor.execute(query, (item['url']))
        result = cursor.fetchone()

        if result != None and len(result) > 0:
            print "[%s] %s duplicate" % (spider.name, datetime.now())
            raise DropItem("Drop duplicate item: %s" % result[0])
        else:
            return item

class MySQLStorePipeline(object):
    def process_item(self, item, spider):
        global conn

        cursor = conn.cursor()
        query = """
            INSERT INTO article(source, url, category, title, content, subtitle, published_at, place, author, fetched_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (item['source'], item['url'], item['category'], item['title'], item['content'], item['subtitle'], item['published_at'], item['place'], item['author']))

        # Print to screen
        print "[%s] %s ok" % (spider.name, datetime.now())

        return item

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item