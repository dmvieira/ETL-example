# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class FaperjItem(Item):
    uri = Field()
    name = Field()
    site = Field()
    kind = Field()
    # TODO definir como identificar o tipo_edital
    # tipo_edital = Field()
