import pymongo

def connect_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["project"]
    return db["val"]

def insert_into_mongo(collection, data):
    if data:
        collection.insert_many(data)
    else:
        print("Empty dictionary")

def delete_from_mongo(collection, user_id):
    query = {"userID": user_id}
    collection.delete_one(query)
