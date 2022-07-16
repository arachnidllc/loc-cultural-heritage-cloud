import json
import math
import re

import scrapy
from loc_crawler.items import LocCrawlerItem


class LocItemImagesSpider(scrapy.Spider):

    name = 'loc_item_images'

    start_urls = ['https://loc.gov/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.file_name = kwargs.get('fn')

    def parse(self, response):
        with open(self.file_name, 'r') as f:
            input_file = json.load(f)
        item_image_urls = self.create_image_urls(items=input_file['items'])
        for loc_item in item_image_urls:
            item = LocCrawlerItem()
            item['item_id'] = loc_item['item_id']
            item['image_urls'] = loc_item['item_image_urls']

            yield item

    def create_image_urls(self, items: list) -> dict:
        URL_TEMPLATE = (
            'https://tile.loc.gov/storage-services/service/pnp/habshaer/{prefix}/{prefix}{item_base}/{item_id}/photos/'
            '{image_id}.jpg'
        )
        item_image_links = []
        for item in items:
            item_id = item['item']['id']
            prefix = item_id[:2]
            item_base_number = math.floor(int(item_id[2:]) / 100) * 100
            image_links = []
            for photo_item in item['aka']:
                photo_id = re.findall(r'(?<=.photos.)([a-z0-9]+)', photo_item)
                if photo_id:
                    full_photo_id = f'{photo_id[0]}v'
                    image_url = URL_TEMPLATE.format(
                        prefix=prefix,
                        item_base=item_base_number,
                        item_id=item_id,
                        image_id=full_photo_id,
                    )
                    image_links.append(image_url)
            item_image_links.append({'item_id': item_id, 'item_image_urls': image_links})
        return item_image_links
