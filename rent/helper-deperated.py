# 填补字段，爬虫脚本更新后就不用了
import pymongo
import requests
#import pandas
from bson.json_util import dumps

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
    collection = db['House']

def add_lnglat():
    houses = list(collection.find())
    for house in houses:
        if 'longitude' in house:
            collection.update({'link': house['link']}, {'$set': {'lnglat': [house['longitude'], house['latitude']]}})

def export_json():
    cursor = collection.find({})
    with open('collection.json', 'w', encoding='utf-8') as file:
        file.write('[')
        for document in cursor:
            del document["lnglat"]
            del document["_id"]
            document["houseNum"] = len(document["houseList"])
            del document["houseList"]
            s = dumps(document, indent=1, ensure_ascii=False)#.encode('utf8')
            file.write(str(s))
            file.write(',')
        file.write(']')

if __name__ == '__main__':
    # get_collection()
    # print('Processing...')
    # add_lnglat()
    # print('Done.')
    get_collection()
    export_json()