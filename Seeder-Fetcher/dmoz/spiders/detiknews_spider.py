from scrapy.selector.libxml2sel import HtmlXPathSelector

from __init__ import *
from dmoz.items import SeedItem
from dmoz.spiders.base_spider import BaseFetcher
from dmoz.spiders.base_spider import BaseSeeder

#
# DETIKNEWS SEEDER
#
class DetiknewsSeeder(BaseSeeder):
    name = "seeder-detiknews"
    source = "detiknews.com"
    start_urls = [
        "http://www.detiknews.com/indeks"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        categories = []
        categories_html = hxs.select('//div[@class="title_3"]')
        for category in categories_html:
            if len(category.select('text()').extract()) > 0:
                categories.append(category.select('text()').extract()[0])

        news_groups = hxs.select('//ul[@class="list_indeks"]')
        items = []
        idx_group = 0
        for news_group in news_groups:
            news_articles = news_group.select('li')
            for news_article in news_articles:
                if len(news_article.select('a/@href').extract()) > 0:
                    item = SeedItem()
                    item['source'] = "detiknews.com"
                    item['category'] = categories[idx_group]
                    item['url'] = news_article.select('a/@href').extract()[0]
                    items.append(item)
            idx_group += 1
        return items

    def normalize_category(self, category_str):
        if category_str.lower() in ('berita'):
            return self.CATEGORY_NATIONAL
        elif category_str.lower() in ('internasional', 'bbc world'):
            return self.CATEGORY_INTERNATIONAL
        else:
            return self.CATEGORY_OTHERS

#
# DETIKNEWS FETCHER
#
class DetiknewsFetcher(BaseFetcher):
    name = "fetcher-detiknews"
    source = "detiknews.com"
    xpath_title = '//div[@class="content_detail"]/h1'
    xpath_content = '//div[@class="text_detail"]/text()'
    xpath_subtitle = '//div[@class="content_detail"]/h2'
    xpath_published_at = '//span[@class="date"]'
    xpath_place = '//div[@class="text_detail"]/strong'
    xpath_author = '//div[@class="author"]/strong'

    def parse_date(self, date_str):
        date_partition = date_str.split(' ')
        dmy_partition = date_partition[1].split('/')
        return "%s-%s-%s %s" % (dmy_partition[2], dmy_partition[1], dmy_partition[0], date_partition[2])
