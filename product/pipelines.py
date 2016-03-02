# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from models import   db_connect, create_deals_table
from items import ProductItem, Test
from models import Test,  db_connect, create_deals_table



# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProductPipeline(object):
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
        '''
        name
        shop_url
        pid
        price
        category
        detail_images
        name
        shop_url
        price
        pid
        buy_color
        thumb_images
        '''
        '''
        product = ProductItem(name=item['name'],
                              shop_url=item['shop_url'],
                              pid=item['pid'],
                              price = item['price'],
                              category = item['category'],
                              detail_images = item['detail_images'],
                              buy_color = item['buy_color'],
                              thumb_images = item['thumb_images']
        )'''
        item = ProductItem(**item)

        print product
        try:
            product.commit_item(engine=engine)
            #session.add(product)
            #session.commit()
        except:
            print "saving failed"
            #session.rollback()
            raise
        #finally:
            #session.close()

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
