# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
    def __init__(self):
        self.ja_processados = []

    def process_item(self, item, spider):
        link = item['uri'].replace('https://', '')
        link = item['uri'].replace('http://', '')
        if link.endswith('/'):
            link = link[:-1]

        if link in self.ja_processados or not item['name']:
            raise DropItem('link ja existe')

        self.ja_processados.append(link)
        return item
