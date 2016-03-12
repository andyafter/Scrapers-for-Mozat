# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from models import   db_connect, create_deals_table
from items import ProductItem
from models import ItemInfo,  db_connect, create_deals_table

from product.utils.config import ALGORITHM_MYSQL_CONFIG
from product.utils.db.simple_db_util import get_db
from product.utils.db.db_cache import InsertProduct
from product.utils.tag_source_process import process_tag_source_dic

import copy
import json
from time import strftime



# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProductPipeline(object):
    DUPLICATE_CHECK = '''
            select id from `product` where pid = {pid} or tag_source = {tag_source}
    '''
    def __init__(self):
        self.db_config = copy.deepcopy(ALGORITHM_MYSQL_CONFIG)
        self.conn = get_db(self.db_config)
        self.write_conn = InsertProduct(5, self.db_config, False)

    def is_duplicated(self, pid, tag_source):
        sql = ProductPipeline.DUPLICATE_CHECK.format(pid='\'' + str(pid) + '\'', tag_source='\'' + str(tag_source) + '\'')
        if self.conn.fetch_row(sql):
            return True
        else:
            return False

    def process_item(self, item, spider):
        new_record = {}
        tag_source = {}
        tag_source['category'] = item['category']
        tag_source['info'] = item['info']
        tag_source['name'] = item['name']
        tag_source['brand'] = item['brand_en']
        tag_source['description'] = item['description']
        tag_source = process_tag_source_dic(tag_source)
        new_record['tag_source'] = json.dumps(tag_source)
        # print new_record['tag_source']
        if self.is_duplicated(item['pid'], new_record['tag_source']):
            return item
        new_record['pid'] = item['pid']
        new_record['update_time'] = str(strftime("%Y-%m-%d %H:%M:%S"))
        new_record['merchant'] = item['merchant']
        detail_url_list = item['detail_image_path'].split('|')
        new_record['suitable_images'] = detail_url_list[int(item['suitable_images_index'])]
        if item['white_suitable_images']:
            new_record['white_suitable'] = detail_url_list[int(item['white_suitable_images_index'])]
        else:
            new_record['white_suitable'] = ''
        new_record['detail_images'] = item['detail_image_path']
        new_record['shop_url'] = item['url']
        new_record['brand_en'] = item['brand_en']
        new_record['merchant_en'] = item['merchant_en']
        new_record['price'] = item['price']
        new_record['discount_price'] = item['discount_price']

        # alright I'm not sure why but you must make sure that this record is
        # not empty in my local database
        #new_record['stock_info'] = 'info'

        if item['discount_price']:
            new_record['discount_percent'] = 100 - (item['discount_price']*100/item['price'])
        else:
            new_record['discount_percent'] = 0
        #print 'Store to database:' + str(new_record)
        for i in new_record:
            print "hhhhhhhhhhhhh"
            print i, type(new_record[i])
        self.write_conn.add(new_record)
        print "stored!!!!!!!"
        return item


class TestPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        deal = Test(**item)

        try:
            session.add(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        print "seems good"
        print item
        return item
