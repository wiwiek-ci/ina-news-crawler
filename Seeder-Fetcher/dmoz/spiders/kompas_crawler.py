from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from __init__ import *
from dmoz.spiders.base_crawler import NewsBaseCrawler

#
# KOMPAS CRAWL
#
class KompasCrawler(NewsBaseCrawler):
    # Identifier
    name = 'kompas'
    source = 'kompas.com'

    # Debug
    debug = False

    # Rules
    allowed_domains = ['kompas.com']
    start_urls = [
        'http://www1.kompas.com/newsindex/secidx/1/nasional/',
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/read/', ), unique=True), follow=True, callback='parse_item'),
    )

    # XPath
    xpath_title = '//div[@class="judul_artikel2011"]'
    xpath_subtitle = '//div[@class="font11 c_orange_kompas2011 pb_5 pt_5"]'
    xpath_category = '//div[@class="menu_kompas"]/ul/li/a[@class="selected"]';
    xpath_author = '//none'
    xpath_published_at = '//none'
    xpath_place = '//div[@class="isi_berita2011 pt_5"]/p/strong'
    xpath_content = '//p'

    # Overriden methods
    def parse_place(self, place_str):
        split_str = place_str.split(',')
        return split_str[0]

    def normalize_category(self, category_str):
        if category_str.lower() in ('nasional', 'regional', 'megapolitan'):
            return self.CATEGORY_NATIONAL
        elif category_str.lower() in ('internasional'):
            return self.CATEGORY_INTERNATIONAL
        elif category_str.lower() in ('bisniskeuangan'):
            return self.CATEGORY_ECONOMY
        elif category_str.lower() in ('olahraga'):
            return self.CATEGORY_SPORTS
        elif category_str.lower() in ('sains'):
            return self.CATEGORY_SCITECH
        elif category_str.lower() in ('travel', 'oase', 'edukasi'):
            return self.CATEGORY_HUMANIORA
        else:
            return self.CATEGORY_OTHERS