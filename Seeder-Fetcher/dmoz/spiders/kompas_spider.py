from __init__ import *
from dmoz.spiders import capitalizeFirstCharInWord
from dmoz.spiders.base_spider import BaseFetcher
from dmoz.spiders.base_spider import BaseSeeder

#
# KOMPAS SEEDER
#
class KompasSeeder(BaseSeeder):
    name = "seeder-kompas"
    source = "kompas.com"
    start_urls = [
        "http://www.kompas.com/getrss/internasional",
        "http://www.kompas.com/getrss/nasional",
        "http://www.kompas.com/getrss/regional",
        "http://www.kompas.com/getrss/megapolitan",
        "http://www.kompas.com/getrss/bisniskeuangan",
        "http://www.kompas.com/getrss/olahraga",
        "http://www.kompas.com/getrss/sains",
        "http://www.kompas.com/getrss/travel",
        "http://www.kompas.com/getrss/oase",
        "http://www.kompas.com/getrss/edukasi"
    ]

    def normalize_category(self, category_str):
        if category_str.lower() in ('589597', 'regional', 'megapolitan'):
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

#
# KOMPAS FETCHER
#
class KompasFetcher(BaseFetcher):
    name = "fetcher-kompas"
    source = "kompas.com"
    xpath_title = '/html/body/div[3]/div[2]/div/div[4]/div/div[3]'
    xpath_content = '//p'
    xpath_subtitle = '/html/body/div[3]/div[2]/div/div[4]/div/div[2]'
    xpath_published_at = '/html/body/div[3]/div[2]/div/div[4]/div/div[6]/div/span[last()]'
    xpath_place = '//p/strong'
    xpath_author = '/html/body/div[3]/div[2]/div/div[4]/div/div[6]/div/span[1]'

    def parse_date(self, date_str):
        date_partition = date_str.split(' ')
        month = ('januari', 'februari', 'maret', 'april', 'mei', 'Juni', 'juli', 'agustus', 'september', 'oktober', 'november', 'desember')
        idx_month = month.index(date_partition[2].lower()) + 1
        return "%s-%s-%s %s" % (date_partition[3], idx_month, date_partition[1], date_partition[5])

    def parse_place(self, place_str):
        place_partition = place_str.partition(',')
        if len(place_partition[1]) > 0:
            return capitalizeFirstCharInWord(place_partition[0].lower())
        else:
            return ''