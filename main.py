import json
import pyjson5 as json5
import pymongo
from pymongo.collection import Collection
import pandas as pd


def saveJsonToMongo(path, collection):
    with open(path, 'r') as file:
        file_data = json.load(file)
    inserted = collection.insert_many(file_data)
    print(inserted.inserted_ids)


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # zakomentovat po vytvřoení
    mydb = myclient["RDBsemestral"]
    mycol = mydb["TollGates"]
    saveJsonToMongo('data/data-export2.json', mycol)
