import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import UniqueConstraint

import settings


DeclarativeBase = declarative_base()
# for this models.py you better check the link here:
# http://newcoder.io/scrape/part-3/


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class ItemInfo(DeclarativeBase):
    __tablename__ = "product"
    # here sqlalchemy have settings for mysql to set integer as 10
    # I'm not gonna put too much limitation on the database table columns
    id = Column(Integer, primary_key=True)
    pid = Column('pid', String(45), unique=True)
    tag_source = Column('tag_source', Text, nullable = False)
    # unless strongly urged I'm not gonna write any nullables
    tas_id = Column('tags_id', Text)
    update_time = Column('update_time', DateTime, nullable = False, default=datetime.datetime.utcnow)
    category = Column('category', Integer, nullable = False, default = 0)
    sub_category = Column('sub_category', Integer, nullable = False, default = 0)
    brand = Column('brand', Integer, nullable = False, default = 0)
    detail_images = Column('detail_images', String(4000), nullable = False)
    thumb_images = Column('thumb_images', String(500), nullable = True)
    suitable_images = Column('suitable_images', String(500), nullable = False)
    white_suitable = Column('white_suitable', String(500), nullable = False)
    tag_status = Column('tag_status', SmallInteger)
    visenze_result = Column('visenze_result', Text)
    merchant = Column('merchant', Integer, nullable=False, default=0)
    koutu = Column('koutu', String(500))
    shop_url = Column('shop_url', String(500))
    brand_en = Column('brand_en', String(45))
    merchant_en = Column('merchant_en', String(45))
    price = Column('price', Integer)
    discount_price = Column('discount_price', Integer)
    discount_percent = Column('discount_percent', Integer)
    buy_size = Column('buy_size', String(500), nullable = False, default='[]')
    buy_color = Column('buy_color', String(500), nullable = False, default='[]')
    stock_info = Column('stock_info', String(1000))
    status = Column('status', String(1000))


class Test(DeclarativeBase):
    __tablename__ = "spidertest"
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
