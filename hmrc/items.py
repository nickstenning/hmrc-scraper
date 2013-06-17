# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class HmrcItem(Item):
    url = Field()
    title = Field()
    desc = Field()
    head = Field()
