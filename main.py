import json
import pymongo
import psycopg2


def saveJsonToMongo(path, collection):
    with open(path, 'r') as file:
        file_data = json.load(file)
    inserted = collection.insert_many(file_data)
    print(inserted.inserted_ids)


def SPZ():
    conn = psycopg2.connect(database="postgres",
                            host="localhost",
                            user="postgres",
                            password="root",
                            port="5432")
    cursor = conn.cursor()
    select_stmt = (
        "SELECT spz FROM Vozidlo"
    )
    cursor.execute(select_stmt)
    spz_results = cursor.fetchall()
    spz_dict = {"spz": []}

    for row in spz_results:
        spz_dict["spz"].append(row[0])

    cursor.close()
    conn.close()
    print(spz_dict)


def MongoToPostgre(collection):
    conn = psycopg2.connect(database="postgres",
                            host="localhost",
                            user="postgres",
                            password="root",
                            port="5432")
    cursor = conn.cursor()
    for document in collection.find({},{ "brana_id": 1,
                                         "prujezd.datum_prujezdu":1,
                                         "prujezd.registrace_vozidla.vozidlo.spz":1,
                                         "prujezd.registrace_vozidla.vozidlo.emisni_trida": 1,
                                         "prujezd.registrace_vozidla.vozidlo.km_sazba":1,
                                         "prujezd.registrace_vozidla.ujete_km":1}):
        # print(document)
        brana_id = int(document["brana_id"])
        datum_prujezdu = int(document["prujezd"]["datum_prujezdu"])
        spz = document["prujezd"]["registrace_vozidla"]["vozidlo"]["spz"]
        emisni_trida = document["prujezd"]["registrace_vozidla"]["vozidlo"]["emisni_trida"]
        km_sazba = int(document["prujezd"]["registrace_vozidla"]["vozidlo"]["km_sazba"])
        ujete_km = int(document["prujezd"]["registrace_vozidla"]["ujete_km"])

        insert_stmt = (
            "INSERT INTO Emisni_trida (typ, sazba) VALUES (%s,%s) ON CONFLICT DO NOTHING"
        )
        data = (emisni_trida, km_sazba)
        cursor.execute(insert_stmt, data)

        insert_stmt = (
            "INSERT INTO Vozidlo (spz, kredit, emisni_trida_typ) VALUES (%s,0,%s) ON CONFLICT DO NOTHING"
        )
        data = (spz,emisni_trida)
        cursor.execute(insert_stmt, data)

        insert_stmt = (
            "INSERT INTO Prujezd (brana_id, datum_prujezdu, ujete_km, vozidlo_spz) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
        )
        data = (brana_id, datum_prujezdu, ujete_km, spz)
        cursor.execute(insert_stmt, data)

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # zakomentovat po vytvřoení
    mydb = myclient["RDBsemestral"]
    mycol = mydb["TollGates"]
    # saveJsonToMongo('data/data-export2.json', mycol)
    # MongoToPostgre(mycol)
    SPZ()