# -*- coding: utf-8 -*-
import scrapy
import sqlite3
import requests

from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ProxyPoolSpider.settings import SQLITE_FILE, SQLITE_TABLE
from ProxyPoolSpider.items import ProxyPoolSpiderItem

class KuaidailiSpider(CrawlSpider):
    name = 'kuaidaili'
    allowed_domains = ['www.kuaidaili.com']
    start_urls = [
        'https://www.kuaidaili.com/free/inha/1/', # 国内高匿代理
        'https://www.kuaidaili.com/free/intr/1/'  # 国内普通代理
    ]
    rules = [
        Rule(
            LinkExtractor(allow=r'free/inha/1?\d/$'),
            follow=True, callback='parse_item'),
        Rule(
            LinkExtractor(allow=r'free/intr/1?\d/$'),
            follow=True, callback='parse_item')
    ]

    def parse_item(self, response):
        for tr in response.css('div[id=list] table tbody tr')[1:]:
            tds = tr.css('td')
            country = 'CN'
            host = tds[0].css('::text').extract_first()
            port = tds[1].css('::text').extract_first()
            anonymous = tds[2].css('::text').extract_first()
            protocal = tds[3].css('::text').extract_first()
            address = tds[4].css('::text').extract_first()
            speed_time = tds[5].css('::text').extract_first()
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
            yield item