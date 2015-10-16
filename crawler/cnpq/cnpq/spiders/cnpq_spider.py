# -*- coding: utf-8 -*-
import re

from scrapy.spider import BaseSpider
from scrapy.selector import Selector

from cnpq.items import CnpqItem


class CnpqSpider(BaseSpider):
    name = "cnpq"
    allowed_domains = ["cnpq.br"]
    start_urls = [
        "http://www.cnpq.br/web/guest/chamadas-publicas?p_p_id=resultadosportlet_WAR_resultadoscnpqportlet_INSTANCE_0ZaM&filtro=abertas",
    ]

    def parse(self, response):

        """CNPQ links are inside <ul class="list-notices ...">
        """

        sel = Selector(response)
        editais = sel.xpath("//ul[contains(@class, 'list-notices')]/li")

        items = []

        for item in editais:
            link = CnpqItem()
            link['name'] = item.xpath("./h3/text()").extract()[0]
            uri = item.xpath(".//a[contains(@class, 'pdfPrimeiro')]/@href").extract()
            if uri:
                link['uri'] = uri[0]
                link['kind'] = 'financiamento'
                link['site'] = 'www.cnpq.br'
                items.append(link)

        return items
