import pymongo

MONGO_URI = '182.92.223.235:27017'
MONGO_DB = 'rent'
MONGO_USER = 'admin'
MONGO_PW = 'xtt576566'
MONGO_COLLECTION = 'House'
MONGO_RAW_COLLECTION = 'RentItem'
collection = None
raw_collection = None

def get_all_houses():
    houses = list(collection.find())
    res = []
    for house in houses:
        res.append({
            'location': house['location'],
            'lnglat': house['lnglat'],
            'number': len(house['houseList'])
        })
    return res
 

def get_houses(bounds):
    houses = []
    for bound in bounds:
        houses.extend(search_bound(bound[0]))
    res = []
    for house in houses:
        res.append({
            'location': house['location'],
            'lnglat': house['lnglat'],
            'number': len(house['houseList'])
        })
    return res


def search_bound(bound):
    bound_str = ''
    for b in bound:
        if bound_str != '':
            bound_str += ','
        bound_str += '[' + b[0] + ',' + b[1] + ']'
    func_str = 'function(){polygonPoints=[' + bound_str + ']; var counter = 0; var i; var xinters; var p1, p2; var pointCount = polygonPoints.length; p1 = polygonPoints[0]; var checkPoint=[Number(this.lnglat[0]), Number(this.lnglat[1])]; for (i = 1; i <= pointCount; i++) { p2 = polygonPoints[i % pointCount]; if (checkPoint[0] > Math.min(p1[0], p2[0]) &&            checkPoint[0] <= Math.max(p1[0], p2[0]) ) { if (checkPoint[1] <= Math.max(p1[1], p2[1])) {  if (p1[0] != p2[0]) { xinters = (checkPoint[0] - p1[0]) * (p2[1] - p1[1]) / (p2[0] - p1[0]) + p1[1];  if (p1[1] == p2[1] || checkPoint[1] <= xinters) { counter++; }  } } } p1 = p2; }  if (counter % 2 == 0) { return false;  } else { return true; } }'
    res = collection.find({'$where': func_str})
    return list(res)

def get_collection():
    global collection
    global raw_collection
    client = pymongo.MongoClient(MONGO_URI, username=MONGO_USER, password=MONGO_PW)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    raw_collection = db[MONGO_RAW_COLLECTION]


# def get_houses(bounds):
#     min_lng = 1000
#     max_lng = 0
#     min_lat = 1000
#     max_lat = 0
#     for bound in bounds:
#         for b in bound[0]:
#             b[0] = float(b[0])
#             b[1] = float(b[1])
#             min_lng = min(b[0], min_lng)
#             max_lng = max(b[0], max_lng)
#             min_lat = min(b[1], min_lat)
#             max_lat = max(b[1], max_lat)
#     print(min_lng)
#     print(max_lng)
#     print(min_lat)
#     print(max_lat)
#     min_lng = str(min_lng)
#     max_lng = str(max_lng)
#     min_lat = str(min_lat)
#     max_lat = str(max_lat)
#     houses = list(collection.find({'longitude':{'$lte': max_lng, '$gte': min_lng}, 'latitude': {'$lte': max_lat, '$gte': min_lat}}))
#     res = []
#     for house in houses:
#         res.append({
#             'location': house['location'],
#             'lnglat': house['lnglat'],
#             'number': len(house['houseList'])
#         })
#     return res   


# def is_in_poly(p, poly):
#     """
#     :param p: [x, y]
#     :param poly: [[], [], [], [], ...]
#     :return:
#     """
#     px, py = p
#     is_in = False
#     for i, corner in enumerate(poly):
#         next_i = i + 1 if i + 1 < len(poly) else 0
#         x1, y1 = corner
#         x2, y2 = poly[next_i]
#         if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
#             is_in = True
#             break
#         if min(y1, y2) < py <= max(y1, y2):  # find horizontal edges of polygon
#             x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
#             if x == px:  # if point is on edge
#                 is_in = True
#                 break
#             elif x > px:  # if point is on left-side of line
#                 is_in = not is_in
#     return is_in