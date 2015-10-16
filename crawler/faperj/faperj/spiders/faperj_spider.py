# -*- coding: utf-8 -*-
import re

from scrapy.spider import BaseSpider
from scrapy.selector import Selector

from faperj.items import FaperjItem


class FaperjSpider(BaseSpider):
    name = "faperj"
    allowed_domains = ["faperj.br"]
    start_urls = [
        "http://www.faperj.br/interna.phtml?obj_id=5196",
    ]

    def parse(self, response):

        """FAPERJ links are inside bold text (html b or strong tags).
        """

        sel = Selector(response)
        divtexto = sel.xpath("//div[@id='texto']")
        bolds = divtexto.xpath(".//b | .//strong")

        items = []

        started_active_announcements_section = False
        for item in bolds:
            text = item.extract()
            lower_text = text.lower()

            # remove html tags
            if not started_active_announcements_section:
                if ('editais' in lower_text
                        and u'lançados' in lower_text
                        and '2013' in lower_text):
                    started_active_announcements_section = True
                continue

            # active announcements ended
            if ('editais' in lower_text
                    and 'prazos' in lower_text
                    and 'encerrados' in lower_text):
                break

            # if item has some link inside it
            subitems = item.xpath(".//a/@href")
            if subitems:
                link = FaperjItem()
                link['uri'] = subitems[0].extract().encode('utf8')

            # if item is inside a link (html a tag)
            ancestors = item.xpath("ancestor::a/@href")
            if ancestors:
                link = FaperjItem()
                link['uri'] = ancestors[0].extract().encode('utf8')

            if 'uri' in link:
                link['name'] = re.sub(
                    '<[^<]+?>', '', item.extract().encode('utf8'))
                link['site'] = 'www.faperj.br'
                link['kind'] = 'misturado'
                items.append(link)

        return items
