# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class SeedItem(Item):
    source = Field()
    category = Field()
    url = Field()

class ArticleItem(Item):
    id = Field()
    source = Field()
    url = Field()
    category = Field()
    title = Field()
    content = Field()
    subtitle = Field()
    published_at = Field()
    place = Field()
    author = Field()