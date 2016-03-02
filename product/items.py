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


class ProductItem(SqlItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sqlmodel = ItemInfo
    # this class seems to be use less anymore
    # I used dirty ways


class Test(Item):
    """Livingsocial container (dictionary-like object) for scraped data"""
    title = Field()
