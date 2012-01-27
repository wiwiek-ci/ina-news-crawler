from __init__ import *
from scrapy.selector.libxml2sel import HtmlXPathSelector
from dmoz.items import ArticleItem
from dmoz.spiders import capitalizeFirstCharInWord
from dmoz.spiders.base_spider import BaseFetcher
from dmoz.spiders.base_spider import BaseSeeder

#
# TEST SEEDER
#
class TestSeeder(BaseSeeder):
    name = "seeder-test"
    source = "site.name"
    start_urls = [
        "http://www.kompas.com/getrss/internasional"
    ]

    def parse(self, response):
        items = super(TestSeeder, self).parse(response)
        print items
        return None

#
# TEST FETCHER
#
class TestFetcher(BaseFetcher):
    name = "fetcher-test"
    source = "kompas.com"
    start_urls = ["http://nasional.kompas.com/read/2012/01/27/17280513/Wa.Ode.Lebih.Besar.dari.Kasus.Nazaruddin"]
    xpath_title = '/html/body/div[3]/div[2]/div/div[4]/div/div[3]'
    xpath_content = '//p'
    xpath_subtitle = '/html/body/div[3]/div[2]/div/div[4]/div/div[2]'
    xpath_published_at = '/html/body/div[3]/div[2]/div/div[4]/div/div[6]/div/span[last()]'
    xpath_place = '//p/strong'
    xpath_author = '/html/body/div[3]/div[2]/div/div[4]/div/div[6]/div/span[1]'

    def __init__(self):
        self.allowed_domains = [self.source]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        # Initilize item
        article = ArticleItem()

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

        # Print value
        print article

        # Return value
        return None