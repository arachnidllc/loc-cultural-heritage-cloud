import json
from datetime import datetime

import scrapy
from scrapy import Request, signals
from scrapy.exceptions import CloseSpider


class LocCollectionsSpider(scrapy.Spider):

    name = 'loc_collections'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.url = kwargs.get('url')
        self.items_limit = int(kwargs.get('items_limit', 500))
        self.result = {'pages': [], 'items': []}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        save_file_path = f'./output/{self.name}_{datetime.utcnow().strftime("%d-%m-%Y_%H:%M:%S")}.json'
        with open(save_file_path, 'w') as output_file:
            json.dump(self.result, output_file)

    def start_requests(self):
        if not self.url:
            raise CloseSpider('Please provide "url" to crawl.')
        yield Request(url=self.url, callback=self.parse)

    def parse(self, response):
        page = response.json()
        if len(self.result['items']) < self.items_limit:
            items = page.pop('results')
            for item in items:
                if len(self.result['items']) < self.items_limit:
                    self.result['items'].append(item)
            self.result['pages'].append(page)

            next_page = page.get('pagination', {}).get('next')
            if next_page:
                yield response.follow(next_page, callback=self.parse)
