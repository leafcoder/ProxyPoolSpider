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
        keys = list(item.fields.keys())
        keys.remove('is_available')
        host = item['host']
        port = item['port']
        is_available = item.pop('is_available')
        cur = self.conn.execute(
            'select count(*) from {0} where host=? and port=?;'.format(
                self.sqlite_table), (host, port))
        size = cur.fetchone()[0]
        if size == 0 and is_available == True:
            spider.log('Insert data: %s' % item)
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
        elif size > 0 and is_available == False:
            spider.log('Delete data: %s' % item)
            delete_sql = "delete from {0} where host=? and port=?;".format(
                self.sqlite_table, )
            try:
                self.conn.execute(delete_sql, (host, port))
                self.conn.commit()
            except:
                self.conn.rollback()
                raise
        elif size > 0 and is_available == True:
            spider.log('Update data: %s' % item)
            update_sql = """\
                update {0} set {1} where host=? and port=?;""".format(
                    self.sqlite_table,
                    ', '.join(['%s=?' % key for key in keys]))
            values = []
            for key in keys:
                values.append(item.get(key))
            values.extend([host, port])
            try:
                self.conn.execute(update_sql, values)
                self.conn.commit()
            except:
                self.conn.rollback()
                raise
            return item
