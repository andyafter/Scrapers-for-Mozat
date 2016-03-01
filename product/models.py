from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

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
    __tablename__ = "hahaha"
    id = Column(Integer, primary_key=True)


class Test(DeclarativeBase):
    __tablename__ = "spidertest"
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
