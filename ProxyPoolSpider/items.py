# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyPoolSpiderItem(scrapy.Item):

    country      = scrapy.Field()
    host         = scrapy.Field()
    port         = scrapy.Field()
    address      = scrapy.Field()
    anonymous    = scrapy.Field()
    protocal     = scrapy.Field()
    speed_time   = scrapy.Field()
    connect_time = scrapy.Field()
    alive_time   = scrapy.Field()
    verify_time  = scrapy.Field()
