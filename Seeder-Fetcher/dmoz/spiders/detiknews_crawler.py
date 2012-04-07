from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from __init__ import *
from dmoz.spiders.base_crawler import NewsBaseCrawler

#
# DETIKNEWS CRAWL
#
class DetiknewsCrawler(NewsBaseCrawler):
    # Identifier
    name = 'detiknews'
    source = 'detiknews.com'

    # Debug
    debug = False

    # Rules
    allowed_domains = ['news.detik.com']
    start_urls = [
        'http://news.detik.com/indeks?ndindeks',
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/read/', ), unique=True), follow=True, callback='parse_item'),
    )

    # XPath
    xpath_title = '//div[@class="content_detail"]/h1'
    xpath_subtitle = '//div[@class="content_detail"]/h2'
    xpath_category = '//div[@class="menu"]/ul/li[@class="selected"]/a';
    xpath_author = '//div[@class="author"]/strong'
    xpath_published_at = '//span[@class="date"]'
    xpath_place = '//div[@class="text_detail"]/strong'
    xpath_content = '//div[@class="text_detail"]/text()'

    # Overriden methods
    def parse_date(self, date_str):
        date_partition = date_str.split(' ')
        dmy_partition = date_partition[1].split('/')
        return "%s-%s-%s %s" % (dmy_partition[2], dmy_partition[1], dmy_partition[0], date_partition[2])

    def normalize_category(self, category_str):
        if category_str.lower() in ('berita'):
            return self.CATEGORY_NATIONAL
        elif category_str.lower() in ('internasional', 'bbc world'):
            return self.CATEGORY_INTERNATIONAL
        else:
            return self.CATEGORY_OTHERS