from datetime import datetime
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector.libxml2sel import HtmlXPathSelector

from __init__ import *
from dmoz.items import ArticleItem
from dmoz.spiders import capitalizeFirstCharInWord
from dmoz.spiders import sanitize

#
# CRAWL SPIDER
#
class NewsBaseCrawler(CrawlSpider):
    # Category
    CATEGORY_NATIONAL = "Nasional"
    CATEGORY_INTERNATIONAL = "Internasional"
    CATEGORY_ECONOMY = "Ekonomi"
    CATEGORY_SPORTS = "Olahraga"
    CATEGORY_FOOTBALL = "Sepakbola"
    CATEGORY_SCITECH = "Iptek"
    CATEGORY_HUMANIORA = "Humaniora"
    CATEGORY_ENTERTAINMENT = "Hiburan"
    CATEGORY_OTHERS = "Lain-lain"

    # Debug
    debug = False

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        # Assign given elements
        article = ArticleItem()
        article['source'] = self.source
        article['url'] = response.url

        # Parse Category
        try:
            category_str = sanitize(self.get_category(response))
            article['category'] = capitalizeFirstCharInWord(self.normalize_category(self.parse_category(category_str)))
        except:
            article['category'] = ''

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
        except:
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

        # Debug
        if self.debug == True:
            print article
            print ''
        else:
            return article

    def parse_date(self, date_str):
        return date_str

    def parse_place(self, place_str):
        return place_str

    def parse_author(self, author_str):
        return author_str

    def get_category(self, response):
        hxs = HtmlXPathSelector(response)
        return hxs.select(self.xpath_category).extract()[0]

    def parse_category(self, category_str):
        return category_str

    def normalize_category(self, category_str):
        return category_str