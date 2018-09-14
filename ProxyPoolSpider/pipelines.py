# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class ProxyPoolSpiderPipeline(object):

    def __init__(self, sqlite_file, sqlite_table):
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file = crawler.settings.get('SQLITE_FILE'),
            sqlite_table = crawler.settings.get('SQLITE_TABLE', 'items')
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)
        self.conn.execute('''
            create table if not exists {0} (
                country      varchar,
                host         varchar,
                port         varchar,
                address      varchar,
                anonymous    varchar,
                protocal     varchar,
                speed_time   varchar,
                connect_time varchar,
                alive_time   varchar,
                verify_time  varchar
            );
        '''.format(self.sqlite_table))
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        keys = item.fields.keys()
        host = item['host']
        port = item['port']
        cur = self.conn.execute(
            'select count(*) from {0} where host=? and port=?;'.format(
                self.sqlite_table), (host, port))
        size = cur.fetchone()[0]
        if size == 0:
            insert_sql = "insert into {0}({1}) values ({2})".format(
                self.sqlite_table,
                ', '.join(keys),
                ', '.join(['?'] * len(keys)))
            values = []
            for key in keys:
                values.append(item.get(key))
            try:
                self.conn.execute(insert_sql, values)
                self.conn.commit()
            except:
                self.conn.rollback()
                raise
        return item