# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.item import Item, Field
from scrapy_sqlitem import SqlItem
from sqlalchemy import Table, MetaData
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, SmallInteger
from product.models import ItemInfo


metadata = MetaData()


class ProductItem(SqlItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sqlmodel = ItemInfo
    '''
    sqlmodel =Table('product', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(45)),
                    Column('pid', String(45), unique=True),
                    Column('tag_source', Text),
    # unless strongly urged I'm not gonna write any nullables
                    Column('tags_id', Text),
                    Column('update_time', DateTime, nullable = False, default=datetime.datetime.utcnow),
                    Column('category', Integer, nullable = False, default = 0),
                    Column('sub_category', Integer, default = 0),
                    Column('brand', Integer, default = 0),
                    Column('detail_images', String(4000)),
                    Column('thumb_images', String(500)),
                    Column('suitable_images', String(500)),
                    Column('white_suitable', String(500), nullable = False),
                    Column('tag_status', SmallInteger),
                    Column('visenze_result', Text),
                    Column('merchant', Integer, default=0),
                    Column('koutu', String(500)),
                    Column('shop_url', String(500)),
                    Column('brand_en', String(45)),
                    Column('merchant_en', String(45)),
                    Column('price', Integer),
                    Column('discount_price', Integer),
                    Column('discount_percent', Integer),
                    Column('buy_size', String(500), default='[]'),
                    Column('buy_color', String(500), nullable = False, default='[]'),
                    Column('stock_info', String(1000)),
                    Column('status', String(1000))
        )
    '''


class Test(Item):
    """Livingsocial container (dictionary-like object) for scraped data"""
    title = Field()
