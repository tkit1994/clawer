# -*- coding: utf-8 -*-
import scrapy
from paper_clawer.items import PaperClawerItem

class Ijcai18Spider(scrapy.Spider):
    name = 'ijcai_18'
    allowed_domains = ['www.ijcai-18.org']
    start_urls = ['https://www.ijcai-18.org/accepted-papers/']

    def parse(self, response):
        result = response.xpath('//*[@id="post-710"]/div/ul/li/text()')
        for i in result:
            title, *authors = i.extract().split(',')
            item = PaperClawerItem()
            item["title"] = title
            item["authors"] = authors
            if "re-id" in title.lower():
                yield item



