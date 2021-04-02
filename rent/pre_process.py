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
    try:
        new_collection.drop()

def generate_dict():
    res = dict()
    lnglat_dict = dict()
    houses = list(collection.find())
    for house in houses:
        if 'lnglat' not in house:
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

    # 合并一下经纬度相同的
    for key in res:
        lnglat = res[key][0]['lnglat']
        if lnglat in lnglat_dict:
            lnglat_dict[lnglat].append(key)
        else:
            lnglat_dict[lnglat] = [key]
    for key in lnglat_dict:
        if len(lnglat_dict[key]) > 1:
            arr = lnglat_dict[key]
            tmp = []
            new_location = ''
            for h in arr:
                if new_location != '':
                    new_location += '&'
                new_location += h
                tmp.extend(res[h])
                del res[h]
            res[new_location] = tmp

    for key in res:
        tmp = res[key][0]['lnglat']
        single = {
            'location': key,
            'lnglat': tmp,
            'longitude': tmp[0],
            'latitude': tmp[1],
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
            collection.update({'link': house['link']}, {'$set': {'lnglat': [info[0], info[1]]}})
            print('updated ' + house['link'])
            house['lnglat'] = [info[0], info[1]]
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