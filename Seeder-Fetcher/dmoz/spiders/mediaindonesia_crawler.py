from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from __init__ import *
from dmoz.spiders.base_crawler import NewsBaseCrawler

#
# MEDIA INDONESIA CRAWL
#
class MediaindonesiaCrawler(NewsBaseCrawler):
    # Identifier
    name = 'mediaindonesia'
    source = 'mediaindonesia.com'

    # Debug
    debug = False

    # Rules
    allowed_domains = ['mediaindonesia.com']
    start_urls = [
        'http://mediaindonesia.com',
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/read/', ), unique=True), follow=True, callback='parse_item'),
    )

    # XPath
    xpath_title = '//div[@class="judul-micom"]'
    xpath_subtitle = '//none'
    xpath_category = '//none';
    xpath_author = '//div[@class="penulis-micom"]/strong'
    xpath_published_at = '//div[@class="tgl_jam-micom"]'
    xpath_place = '//div[@id="baca"]/div/span'
    xpath_content = '//div[@id="baca"]/div[7]'

    # Overriden methods
    def parse_date(self, date_str):
        split_str = date_str.split(' ')

        year = split_str[4]

        if split_str[3] == 'Januari':
            month = '01'
        elif split_str[3] == 'Pebruari' or split_str[2] == 'Februari':
            month = '02'
        elif split_str[3] == 'Maret':
            month = '03'
        elif split_str[3] == 'April':
            month = '04'
        elif split_str[3] == 'Mei':
            month = '05'
        elif split_str[3] == 'Juni':
            month = '06'
        elif split_str[3] == 'Juli':
            month = '07'
        elif split_str[3] == 'Agustus':
            month = '08'
        elif split_str[3] == 'September':
            month = '09'
        elif split_str[3] == 'Oktober':
            month = '10'
        elif split_str[3] == 'November' or split_str[2] == 'Nopember':
            month = '11'
        elif split_str[3] == 'Desember':
            month = '12'
        else:
            return ''

        day = split_str[2]

        time = split_str[5]
        return "%s-%s-%s %s:00" % (year, month, day, time)

    def parse_place(self, place_str):
        split_str = place_str.split(',')
        split_str = split_str[0].split('-')
        return split_str[0]

    def get_category(self, response):
        url_split = response.url.split('/')
        return url_split[8]

    def normalize_category(self, category_str):
        if category_str.lower() in ('284', '5', '35', '37', '38', '101', '126', '289', '127', '290'):
            return self.CATEGORY_NATIONAL
        elif category_str.lower() in ('6', '39', '40'):
            return self.CATEGORY_INTERNATIONAL
        elif category_str.lower() in ('2', '4', '21', '20'):
            return self.CATEGORY_ECONOMY
        elif category_str.lower() in ('3', '285', '286', '289', '149'):
            return self.CATEGORY_SPORTS
        elif category_str.lower() in ('4', '287', '33', '150'):
            return self.CATEGORY_FOOTBALL
        elif category_str.lower() in ('7', '291', '292'):
            return self.CATEGORY_SCITECH
        elif category_str.lower() in ('65'):
            return self.CATEGORY_ENTERTAINMENT
        elif category_str.lower() in ('14', '293', '89'):
            return self.CATEGORY_HUMANIORA
        else:
            return self.CATEGORY_OTHERS