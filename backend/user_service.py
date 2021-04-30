import pymongo

MONGO_URI = '182.92.223.235:27017'
MONGO_DB = 'rent'
MONGO_USER = 'admin'
MONGO_PW = 'xtt576566'
MONGO_COLLECTION = 'User'
collection = None

def get_collection():
    global collection
    global raw_collection
    client = pymongo.MongoClient(MONGO_URI, username=MONGO_USER, password=MONGO_PW)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

def register(uname, pw):
    if collection.find_one({'username': uname}) != None:
        return 0 # has existed
    else:
        collection.insert({
            'username': uname,
            'password': pw,
            'stars': []
            })
        return 1 # ok

def login(uname, pw):
    if collection.find_one({'username': uname, 'password': pw}) != None:
        return 1 # ok
    else:
        return 0 # fail

def star_house(uname, pw, link):
    info = collection.find_one({'username': uname, 'password': pw})
    if info == None:
        return 0    # havent login
    favorites = info['stars']
    if link in favorites:
        return -1   # already stared
    else:
        favorites.append(link)
        collection.update({'username': uname}, {'$set': {'stars': favorites}})
        return 1    # ok

def get_stars(uname, pw):
    info = collection.find_one({'username': uname, 'password': pw})
    if info == None:
        return None    # havent login
    favorites = info['stars']
    return favorites

def remove_star(uname, pw, link):
    info = collection.find_one({'username': uname, 'password': pw})
    if info == None:
        return 0    # havent login
    favorites = info['stars']
    favorites.remove(link)
    collection.update({'username': uname}, {'$set': {'stars': favorites}})
    return 1    # ok    