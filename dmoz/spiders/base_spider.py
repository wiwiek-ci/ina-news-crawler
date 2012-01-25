from datetime import datetime
from scrapy.selector.libxml2sel import HtmlXPathSelector
from scrapy.spider import BaseSpider

from __init__ import *
from dmoz.items import ArticleItem
from dmoz.items import SeedItem
from dmoz.spiders import capitalizeFirstCharInWord
from dmoz.spiders import conn
from dmoz.spiders import sanitize
import feedparser

#
# BASE SEEDER
#
class BaseSeeder(BaseSpider):
    name = None
    source = None
    start_urls = None

    def __init__(self):
        self.allowed_domains = [self.source]

    def parse(self, response):
        category = self.parse_category(response)
        feed = response.body
        items = []
        d = feedparser.parse(feed)
        for entry in d['entries']:
            item = SeedItem()
            item['source'] = self.source
            item['category'] = category
            item['url'] = entry.link
            items.append(item)
        return items

    def parse_category(self, response):
        return response.url.rpartition('/')[2]

#
# BASE FETCHER
#
class BaseFetcher(BaseSpider):
    name = '//none'
    source = '//none'
    xpath_title = '//none'
    xpath_content = '//none'
    xpath_subtitle = '//none'
    xpath_published_at = '//none'
    xpath_place = '//none'
    xpath_author = '//none'

    global conn

    def __init__(self):
        self.allowed_domains = [self.source]
        self.start_urls = []

        cursor = conn.cursor()
        query = """
            SELECT id, source, category, url
            FROM seed
            WHERE status = 'new'
            AND source = %s
            ORDER BY inserted_at DESC
            LIMIT 1
        """
        cursor.execute(query, (self.source))
        result = cursor.fetchone()
        if result != None:
            self.id = result[0]
            self.source = result[1]
            self.category = result[2]
            self.start_urls.append(result[3])

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        # Assign given elements
        article = ArticleItem()
        article['id'] = self.id
        article['source'] = self.source
        article['url'] = response.url
        article['category'] = self.category

        # Parse Title
        try:
            article['title'] = sanitize(hxs.select(self.xpath_title).extract()[0])
        except:
            article['title'] = ''

        # Parse Content
        paragraphs = hxs.select(self.xpath_content).extract()
        lines = []
        for paragraph in paragraphs:
            line = sanitize(paragraph)
            if len(line) > 0:
                lines.append(line)
        article['content'] = '\n'.join(lines)

        # Parse Subtitle
        try:
            article['subtitle'] = capitalizeFirstCharInWord(sanitize(hxs.select(self.xpath_subtitle).extract()[0]))
        except:
            article['subtitle'] = ''

        # Parse Published_at
        try:
            date_str = sanitize(hxs.select(self.xpath_published_at).extract()[0])
            article['published_at'] = self.parse_date(date_str)
        except IndexError:
            article['published_at'] = ''

        # Parse Place
        try:
            place_str = sanitize(hxs.select(self.xpath_place).extract()[0])
            article['place'] = capitalizeFirstCharInWord(self.parse_place(place_str))
        except:
            article['place'] = ''

        # Parse Author
        try:
            author_str = sanitize(hxs.select(self.xpath_author).extract()[0])
            article['author'] = capitalizeFirstCharInWord(self.parse_author(author_str))
        except:
            article['author'] = ''

        # Return value
        return article

    def parse_date(self, date_str):
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    def parse_place(self, place_str):
        return place_str

    def parse_author(self, author_str):
        return author_str