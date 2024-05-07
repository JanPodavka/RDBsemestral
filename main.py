import json
import pymongo
import psycopg2
from pprint import pprint

def saveJsonToMongo(path, collection):
    with open(path, 'r') as file:
        file_data = json.load(file)
    inserted = collection.insert_many(file_data)
    print(inserted.inserted_ids)


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # zakomentovat po vytvřoení
    mydb = myclient["RDBsemestral"]
    mycol = mydb["TollGates"]
    # saveJsonToMongo('data/data-export2.json', mycol)


cursor = mycol.find()
for document in cursor:
    pprint(document)

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="root",
                        port="5432")

cursor = conn.cursor()
