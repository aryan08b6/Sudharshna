from pymongo import MongoClient
from logCollector import getLog

try:
    conn = MongoClient()
    print("Connected Successfully")

    db = conn.Logs

    collection = db.Application_Logs

    for x in getLog("Application", 20):
        collection.insert_one(x)
except:
    print("Ye kya bakchodi hai")



