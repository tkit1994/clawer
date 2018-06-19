# -*- coding: utf-8 -*-
import scrapy
from paper_clawer.items import PaperClawerItem
from scrapy.http.response import urljoin

class ArxivSpider(scrapy.Spider):
    name = 'arxiv'
    allowed_domains = ['arxiv.org']
    start_urls = ['https://arxiv.org/list/cs.CV/180{}?show=1000'.format(i) for i in range(1,6)]

    def parse(self, response):
        dt = response.xpath('//*[@id="dlpage"]/dl/dt')
        dd = response.xpath('//*[@id="dlpage"]/dl/dd')
        for idt, idd in zip(dt, dd):
            url = idt.xpath(
                './span/a[@title="Download PDF"]/@href').extract_first()
            authors = idd.xpath(
                './/div[@class="list-authors"]/a/text()').extract()
            title = idd.xpath(
                './/div[@class="list-title mathjax"]/text()').extract()[-1]
            if "re-id" in title.lower():
                item = PaperClawerItem()
                item["url"] = urljoin(response.url,url)
                item["authors"] = authors
                item["title"] = title.strip()
                yield item



