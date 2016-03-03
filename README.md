# Scrapers

This repository is written with scrapy.

- createdb crawler(if you are using postgresql)
- pip install -r requirements.txt

## About Database
Actually you can run on MySQL by switching to mysql branch, then change the password.


Of course if you want to use Postgresql you can also run **postsql.sh** to start database in your local machine(just for my own convenience). I used SQLAlchemy so if anyone wants to change the database you will have to do some modifications based on that. If nobody wants to do it, you can leave it to me.


## Database Record Meanings
suitable image: First picture when you go to the product detail pge;
white suitable: Clothes picture without a model;
tag status:
merchat: hardcode it
merchant*en: you can also hard code
brand_en: when you crawl a website with clothes coming from other brands;
price: how many cents, not dollars
discount price: price after discount
discount: how many percentage off. Like in modafinilcat;
buy_size  and buy color belongs to job 2;
stock info: {color+size : number }
tag_source: category, info, brand; exactly copy from brand_en
tag_id: except for tag_source, everything else that start with tag you don't have to care;



## Several scripts:
asos spider
asos stock info(deja stock)
young_hungry_free.json used in configurable_scrapy.py
Configurable_spider
spider_pipeline.py


## Noticable:
XHR spider functions
