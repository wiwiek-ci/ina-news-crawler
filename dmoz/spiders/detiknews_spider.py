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
        categories_html = hxs.select('/html/body/div[2]/div[2]/div/h4')
        for category in categories_html:
            if len(category.select('text()').extract()) > 0:
                categories.append(category.select('text()').extract()[0])

        news_groups = hxs.select('/html/body/div[2]/div[2]/div/ul')
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

#
# DETIKNEWS FETCHER
#
class DetiknewsFetcher(BaseFetcher):
    name = "fetcher-detiknews"
    source = "detiknews.com"
    xpath_title = '//div[@id="isiberita"]/span[@class="judul"]'
    xpath_content = '//div[@id="isiberita"]/text()'
    xpath_subtitle = '//span[@class="subjudul"]'
    xpath_published_at = '//span[@class="date"]'
    xpath_place = '//div[@id="isiberita"]/strong'
    xpath_author = '//span[@class="reporter"]/strong'

    def parse_date(self, date_str):
        date_partition = date_str.split(' ')
        dmy_partition = date_partition[1].split('/')
        return "%s-%s-%s %s" % (dmy_partition[2], dmy_partition[1], dmy_partition[0], date_partition[2])
