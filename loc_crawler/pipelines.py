from scrapy.pipelines.images import ImagesPipeline


class LocCrawlerPipeline:
    def process_item(self, item, spider):
        return item


class LocImageSavePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = request.url.split('/')[-1]
        item_folder_name = item['item_id']
        image_filename = f'{item_folder_name}/{image_name}'

        return image_filename
