# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
import os
from paper_clawer.settings import FILES_STORE
class PaperClawerPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonPipeline(object):
    def __init__(self):
        self.file = open("result.json", 'wb')
        self.exporter = JsonItemExporter(
            self.file, encoding='utf-8', ensure_ascii=False, indent=4)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class PdfPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        url = item[self.files_urls_field].replace(
            "https://arxiv.org", "http://cn.arxiv.org")+".pdf"
        return Request(url)

    def item_completed(self, results, item, info):
        file_path = [x["path"] for ok, x in results if ok]
        if file_path:
            os.rename(os.path.join(FILES_STORE, file_path[0]), os.path.join(FILES_STORE, "full", item["title"]+".pdf"))
        return item
