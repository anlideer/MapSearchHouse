import pymongo

MONGO_URI = '123.56.90.234:27017'
MONGO_DB = 'rent'
MONGO_USER = 'anlideer'
MONGO_PW = 'xtt576566'
MONGO_COLLECTION = 'House'
MONGO_RAW_COLLECTION = 'RentItem'
collection = None
raw_collection = None


def get_house_list(name):
    house = collection.find_one({'location': name})
    if house:
        #print(house['houseList'], file=sys.stdout)
        res = house['houseList']
        for h in res:
            # 删掉一些前端不需要的属性
            del h['_id']
            del h['lnglat']
            del h['longitude']
            del h['latitude']
        return res
    else:
        return []

def get_house_by_link(link):
    house = raw_collection.find_one({'link': link})
    return house

# def get_all_houses():
#     houses = list(collection.find())
#     res = []
#     for house in houses:
#         res.append({
#             'location': house['location'],
#             'lnglat': house['lnglat'],
#             'number': len(house['houseList'])
#         })
#     return res
 

# def get_houses(bounds):
#     houses = []
#     for bound in bounds:
#         houses.extend(search_bound(bound[0]))
#     res = []
#     for house in houses:
#         res.append({
#             'location': house['location'],
#             'lnglat': house['lnglat'],
#             'number': len(house['houseList'])
#         })
#     return res


# def search_bound(bound):
#     bound_str = ''
#     for b in bound:
#         if bound_str != '':
#             bound_str += ','
#         bound_str += '[' + b[0] + ',' + b[1] + ']'
#     func_str = 'function(){polygonPoints=[' + bound_str + ']; var counter = 0; var i; var xinters; var p1, p2; var pointCount = polygonPoints.length; p1 = polygonPoints[0]; var checkPoint=[Number(this.lnglat[0]), Number(this.lnglat[1])]; for (i = 1; i <= pointCount; i++) { p2 = polygonPoints[i % pointCount]; if (checkPoint[0] > Math.min(p1[0], p2[0]) &&            checkPoint[0] <= Math.max(p1[0], p2[0]) ) { if (checkPoint[1] <= Math.max(p1[1], p2[1])) {  if (p1[0] != p2[0]) { xinters = (checkPoint[0] - p1[0]) * (p2[1] - p1[1]) / (p2[0] - p1[0]) + p1[1];  if (p1[1] == p2[1] || checkPoint[1] <= xinters) { counter++; }  } } } p1 = p2; }  if (counter % 2 == 0) { return false;  } else { return true; } }'
#     res = collection.find({'$where': func_str})
#     return list(res)

def get_collection():
    global collection
    global raw_collection
    client = pymongo.MongoClient(MONGO_URI, username=MONGO_USER, password=MONGO_PW)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    raw_collection = db[MONGO_RAW_COLLECTION]