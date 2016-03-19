from src.spiders.spider_pipeline import ProductPipeline as ProductPipline
from os.path import join


# class BershkaTagPipeline(TagPipline):
#     def process_item(self, item, spider):
#         data_diretory = join(RAW_INFO_TAG_ROOT, GAP_DATA_DIRECTORY)
#         TagPipline.process_item(self, item, spider, data_diretory)
#         return item

class BershkaProductPipeline(ProductPipline):
    def process_item(self, item, spider):
        ProductPipline.process_item(self, item, spider)
        return item
