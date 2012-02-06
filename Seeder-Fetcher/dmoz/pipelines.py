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
        # Seeder
        if spider.name.find("seeder-") == 0:
            if item['url'] != None and len(item['url']) > 0:
                return item
            else:
                raise DropItem("Drop false seed: %s" % item['id'])
        # Fetcher
        elif spider.name.find("fetcher-") == 0:
            if len(item['title']) > 0 and len(item['content']) > 0:
                status = "ok"
            else:
                status = "err"
            cursor = conn.cursor()
            query = """
                UPDATE seed
                SET fetched_by = %s, fetched_at = NOW(), status = %s
                WHERE id = %s
            """
            cursor.execute(query, (spider.name, status, item['id']))

            # Print to screen
            print "[%s] %s Fetch %s: %s" % (spider.name, datetime.now(), item['id'], status)

            if status == "ok":
                return item
            else:
                raise DropItem("Drop false article: %s" % item['id'])

class DuplicatePipeline(object):
    def process_item(self, item, spider):
        global conn
        # Seeder
        if spider.name.find("seeder-") == 0:
            cursor = conn.cursor()
            query = """
                SELECT url
                FROM seed
                WHERE url = %s
            """
            cursor.execute(query, (item['url']))
            result = cursor.fetchone()

            if result != None and len(result) > 0:
                raise DropItem("Drop duplicate item: %s" % result[0])
            else:
                # Print to screen
                print "[%s] %s Seeds %s" % (spider.name, datetime.now(), item['url'])
                return item
        # Fetcher
        elif spider.name.find("fetcher-") == 0:
            # Do not check duplicate
            return item

class MySQLStorePipeline(object):
    def process_item(self, item, spider):
        global conn
        # Seeder
        if spider.name.find("seeder-") == 0:
            cursor = conn.cursor()
            query = """
                INSERT INTO seed(source, category, url, inserted_by, inserted_at)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(query, (item['source'], item['category'], item['url'], spider.name))
            return item
        # Fetcher
        elif spider.name.find("fetcher-") == 0:
            # Delete in case
            cursor = conn.cursor()
            query = """
                DELETE FROM article
                WHERE id = %s
            """
            cursor.execute(query, (item['id']))

            # Then insert
            cursor = conn.cursor()
            query = """
                INSERT INTO article(id, source, url, category, title, content, subtitle, published_at, place, author, is_gathered)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)
            """
            cursor.execute(query, (item['id'], item['source'], item['url'], item['category'], item['title'], item['content'], item['subtitle'], item['published_at'], item['place'], item['author']))
            return item

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item