import json
import pymongo
import psycopg2


def saveJsonToMongo(path, collection):
    with open(path, 'r') as file:
        file_data = json.load(file)
    inserted = collection.insert_many(file_data)
    print(inserted.inserted_ids)


def readMongo(collection):
    for document in collection.find({},{ "brana_id": 1,
                                         "prujezd.datum_prujezdu":1,
                                         "prujezd.registrace_vozidla.vozidlo.spz":1,
                                         "prujezd.registrace_vozidla.vozidlo.emisni_trida": 1,
                                         "prujezd.registrace_vozidla.vozidlo.km_sazba":1,
                                         "prujezd.registrace_vozidla.ujete_km":1}):
        # print(document)
        brana_id = document["brana_id"]
        datum_prujezdu = document["prujezd"]["datum_prujezdu"]
        spz = document["prujezd"]["registrace_vozidla"]["vozidlo"]["spz"]
        km_sazba = document["prujezd"]["registrace_vozidla"]["vozidlo"]["km_sazba"]
        ujete_km = document["prujezd"]["registrace_vozidla"]["ujete_km"]


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # zakomentovat po vytvřoení
    mydb = myclient["RDBsemestral"]
    mycol = mydb["TollGates"]
    # saveJsonToMongo('data/data-export2.json', mycol)
    readMongo(mycol)

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="root",
                        port="5432")

cursor = conn.cursor()
