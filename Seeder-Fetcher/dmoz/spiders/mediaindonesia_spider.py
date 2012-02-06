from __init__ import *
from dmoz.spiders import capitalizeFirstCharInWord
from dmoz.spiders.base_spider import BaseFetcher
from dmoz.spiders.base_spider import BaseSeeder

#
# MEDIAINDONESIA SEEDER
# 
class MediaindonesiaSeeder(BaseSeeder):
    name = "seeder-mediaindonesia"
    source = "mediaindonesia.com"
    start_urls = [
        "http://www.mediaindonesia.com/rss/1/politik",
        "http://www.mediaindonesia.com/rss/2/ekonomi",
        "http://www.mediaindonesia.com/rss/3/olahraga",
        "http://www.mediaindonesia.com/rss/4/sepakbola",
        "http://www.mediaindonesia.com/rss/5/megapolitan",
        "http://www.mediaindonesia.com/rss/6/mancanegara",
        "http://www.mediaindonesia.com/rss/7/iptek",
        "http://www.mediaindonesia.com/rss/10/hiburan",
        "http://www.mediaindonesia.com/rss/11/opini",
        "http://www.mediaindonesia.com/rss/14/humaniora"
    ]

    def normalize_category(self, category_str):
        if category_str.lower() in ('590285', '590289', 'tanahair'):
            return self.CATEGORY_NATIONAL
        elif category_str.lower() in ('590290'):
            return self.CATEGORY_INTERNATIONAL
        elif category_str.lower() in ('590286'):
            return self.CATEGORY_ECONOMY
        elif category_str.lower() in ('590287'):
            return self.CATEGORY_SPORTS
        elif category_str.lower() in ('590288'):
            return self.CATEGORY_FOOTBALL
        elif category_str.lower() in ('590291'):
            return self.CATEGORY_SCITECH
        elif category_str.lower() in ('590294'):
            return self.CATEGORY_ENTERTAINMENT
        elif category_str.lower() in ('590295', '590292'):
            return self.CATEGORY_HUMANIORA
        else:
            return self.CATEGORY_OTHERS

#
# MEDIAINDONESIA FETCHER
#
class MediaindonesiaFetcher(BaseFetcher):
    name = "fetcher-mediaindonesia"
    source = "mediaindonesia.com"
    xpath_title = '//div[@class="judul"]/h3'
    xpath_content = '//div[@class="baca"]/p'
    xpath_subtitle = '//div[@class="subtit"]'
    xpath_published_at = '//div[@class="tgl"]'
    xpath_place = '//div[@class="baca"]/p/b'
    xpath_author = '//none'

    def parse_date(self, date_str):
        date_partition = date_str.split(' ')
        month = ('januari', 'februari', 'maret', 'april', 'mei', 'Juni', 'juli', 'agustus', 'september', 'oktober', 'november', 'desember')
        try:
            idx_month = month.index(date_partition[3].lower()) + 1
            return "%s-%s-%s %s" % (date_partition[4], idx_month, date_partition[2], date_partition[5])
        except:
            idx_month = month.index(date_partition[1].lower()) + 1
            return "%s-%s-%s %s" % (date_partition[2], idx_month, date_partition[0], date_partition[3])
            

    def parse_place(self, place_str):
        place_partition = place_str.partition('--')
        if len(place_partition[1]) > 0:
            return capitalizeFirstCharInWord(place_partition[0].lower())
        else:
            return ''
        