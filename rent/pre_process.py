import pymongo
import requests

MONGO_URI = '182.92.223.235:27017'
MONGO_DB = 'rent'
MONGO_USER = 'admin'
MONGO_PW = 'xtt576566'

client = None
collection = None
new_collection = None

def get_collection():
    global collection
    global new_collection
    global client
    client = pymongo.MongoClient(MONGO_URI, username=MONGO_USER, password=MONGO_PW)
    db = client[MONGO_DB]
    collection = db['RentItem']
    new_collection = db['House']

def generate_dict():
    res = dict()
    houses = list(collection.find())
    for house in houses:
        if 'longitude' not in house:
            new_house = get_gps(house)
            if new_house != None:
                house = new_house
            else:
                continue
        location = '-'.join(house['location'])
        if location in res:
            res[location].append(house)
        else:
            res[location] = [house]

    for key in res:
        single = {
            'location': key,
            'longitude': res[key][0]['longitude'],
            'latitude': res[key][0]['latitude'],
            'houseList': res[key]
        }
        new_collection.insert(single)

def get_gps(house):
    location = house['location'][0] + ' ' + house['location'][-1]
    try:
        # get longitude and latitude
        url = 'https://restapi.amap.com/v3/geocode/geo'
        params = {
            'key': 'eba3e6f19de198bbf4d41ab24e628f6f',
            'address': location,
            'city': '北京'
        }
        r = requests.get(url, params=params)
        res = r.json()
        if res['status'] == '1':
            geo = res['geocodes'][0]
            info = geo['location'].split(',')
            collection.update({'link': house['link']}, {'$set': {'longitude': info[0], 'latitude': info[1]}})
            print('updated ' + house['link'])
            house['longitude'] = info[0]
            house['latitude'] = info[1]
            return house
    except Exception as e:
        print('ERROR fetching longitude and latitude')
        print(e)
        return None

if __name__ == '__main__':
    get_collection()
    print('processing...')
    generate_dict()
    client.close()