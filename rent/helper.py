# 填补字段，爬虫脚本更新后就不用了
import pymongo
import requests

MONGO_URI = '182.92.223.235:27017'
MONGO_DB = 'rent'
MONGO_USER = 'admin'
MONGO_PW = 'xtt576566'

client = None
collection = None

def get_collection():
    global collection
    global client
    client = pymongo.MongoClient(MONGO_URI, username=MONGO_USER, password=MONGO_PW)
    db = client[MONGO_DB]
    collection = db['RentItem']

def add_lnglat():
    houses = list(collection.find())
    for house in houses:
        if 'longitude' in house:
            collection.update({'link': house['link']}, {'$set': {'lnglat': [house['longitude'], house['latitude']]}})

if __name__ == '__main__':
    get_collection()
    print('Processing...')
    add_lnglat()
    print('Done.')