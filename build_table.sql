DROP DATABASE IF EXISTS algorithm;
create database algorithm;
use algorithm;
CREATE TABLE `product` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `pid` varchar(45) NOT NULL DEFAULT '',
  `tag_source` text NOT NULL,
  `tags_id` varchar(4000) NOT NULL DEFAULT '',
  `update_time` varchar(45) DEFAULT '',
  `category` int(10) unsigned DEFAULT '0',
  `sub_category` int(10) unsigned DEFAULT '0',
  `brand` int(10) unsigned NOT NULL DEFAULT '0',
  `detail_images` varchar(4000) NOT NULL DEFAULT '',
  `thumb_images` varchar(500) DEFAULT '',
  `suitable_images` varchar(500) NOT NULL DEFAULT '',
  `white_suitable` varchar(500) NOT NULL DEFAULT '',
  `tag_status` smallint(5) unsigned DEFAULT NULL,
  `visenze_result` text,
  `merchant` int(10) unsigned NOT NULL DEFAULT '0',
  `koutu` varchar(500) DEFAULT '',
  `shop_url` varchar(500) NOT NULL DEFAULT '',
  `brand_en` varchar(45) DEFAULT NULL,
  `merchant_en` varchar(45) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `discount_price` int(11) DEFAULT NULL,
  `discount_percent` int(7) DEFAULT NULL,
  `buy_size` varchar(500) NOT NULL DEFAULT '[]',
  `buy_color` varchar(500) NOT NULL DEFAULT '[]',
  `stock_info` varchar(1000) NOT NULL DEFAULT '',
  `buy_size_type` varchar(100) DEFAULT NULL,
  `status` int(10) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pid_unique` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=22637 DEFAULT CHARSET=utf8 ;
