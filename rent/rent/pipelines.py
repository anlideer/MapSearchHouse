# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import requests

class RentPipeline:
    def process_item(self, item, spider):
        try:
            # get longitude and latitude
            url = 'https://restapi.amap.com/v3/geocode/geo'
            params = {
                'key': 'eba3e6f19de198bbf4d41ab24e628f6f',
                'address': ''.join(item['location']),
                'city': '北京'
            }
            r = requests.get(url, params=params)
            res = r.json()
            if res['status'] == '1':
                geo = res['geocodes'][0]
                info = geo['location'].split(',')
                item['longitude'] = info[0]
                item['latitude'] = info[1]
        except Exception as e:
            print('ERROR fetching longitude and latitude')
            print(e)
        print(item)
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_user, mongo_pw):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_user = mongo_user
        self.mongo_pw = mongo_pw

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_user = crawler.settings.get('MONGO_USER'),
            mongo_pw=  crawler.settings.get('MONGO_PW')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, username=self.mongo_user, password=self.mongo_pw)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()