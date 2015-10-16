# -*- coding: utf-8 -*-
import re

from scrapy.spider import BaseSpider
from scrapy.selector import Selector

from nsf.items import NsfItem


class NsfSpider(BaseSpider):
    name = "nsf"
    allowed_domains = ["nsf.br"]
    start_urls = [
        "http://www.nsf.gov/funding/pgm_list.jsp?ord=rcnt&org=IIA&status=1&org=IIA",
    ]

    def parse(self, response):

        """NSF links are inside <ul class="list-notices ...">
        """

        sel = Selector(response)
        editais = sel.xpath("//a[@class='atemphover']")

        items = []

        for item in editais:
            link = NsfItem()
            link['name'] = item.xpath("./text()").extract()[0]
            link['uri'] = "http://www.nsf.gov" + item.xpath("./@href").extract()[0]
            link['kind'] = 'cooperacao'
            link['site'] = 'www.nsf.br'
            items.append(link)

        return items
