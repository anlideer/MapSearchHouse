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
            'password': pw
            })
        return 1 # ok

def login(uname, pw):
    if collection.find_one({'username': uname, 'password': pw}) != None:
        return 1 # ok
    else:
        return 0 # fail