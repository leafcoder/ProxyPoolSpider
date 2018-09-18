# -*- coding: utf-8 -*-
import scrapy
import sqlite3
import requests

from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ProxyPoolSpider.settings import SQLITE_FILE, SQLITE_TABLE
from ProxyPoolSpider.items import ProxyPoolSpiderItem

class XicidailiSpider(CrawlSpider):
    name = 'xicidaili'
    allowed_domains = ['www.xicidaili.com']
    start_urls = [
        'http://www.xicidaili.com/nn/1' # 国内高匿代理
    ]
    rules = [
        Rule(LinkExtractor(
            allow=r'nn/1?\d$'), follow=True, callback='parse_item'),
    ]

    def parse_item(self, response):
        for tr in response.css('table[id=ip_list] tr')[1:]:
            tds = tr.css('td')
            country = tds[0].css('img::attr(alt)').extract_first()
            host = tds[1].css('::text').extract_first()
            port = tds[2].css('::text').extract_first()
            address = tds[3].css('a::text').extract_first()
            anonymous = tds[4].css('::text').extract_first()
            protocal = tds[5].css('::text').extract_first()
            speed_time = tds[6].css(
                '.bar_inner::attr(style)').re(r'width:(\d+\%)')[0]
            connect_time = tds[7].css(
                '.bar_inner::attr(style)').re(r'width:(\d+\%)')[0]
            alive_time = tds[8].css('::text').extract_first()
            verify_time = tds[9].css('::text').extract_first()
            item = ProxyPoolSpiderItem()
            try:
                requests.get('http://www.baidu.com/',
                    proxies={'http': 'http://%s:%s' % (host, port)},
                    timeout=5.0
                )
            except:
                self.log('connect to "%s:%s" failed' % (host, port))
                item['is_available'] = False
            else:
                item['is_available'] = True
            item['country'] = country
            item['host'] = host
            item['port'] = port
            item['address'] = address
            item['anonymous'] = anonymous
            item['protocal'] = protocal
            item['speed_time'] = speed_time
            item['connect_time'] = connect_time
            item['alive_time'] = alive_time
            item['verify_time'] = verify_time
            yield item