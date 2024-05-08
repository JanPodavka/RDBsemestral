import json
import pymongo
import psycopg2
from datetime import datetime
import random


def connectToPostgreDb():
    conn = psycopg2.connect(database="postgres",
                            host="localhost",
                            user="postgres",
                            password="root",
                            port="5432")
    return conn, conn.cursor()


def closePostgreDb(conn, cursor):
    cursor.close()
    conn.close()


def saveJsonToMongo(path, collection):
    with open(path, 'r') as file:
        file_data = json.load(file)
    inserted = collection.insert_many(file_data)
    print(inserted.inserted_ids)


def SPZ():
    conn, cursor = connectToPostgreDb()
    select_stmt = (
        "SELECT spz FROM Vozidlo"
    )
    cursor.execute(select_stmt)
    spz_results = cursor.fetchall()
    spz_dict = {"spz": []}

    for row in spz_results:
        spz_dict["spz"].append(row[0])

    closePostgreDb(conn, cursor)
    return spz_dict


def SPZ_Data(spz):
    conn, cursor = connectToPostgreDb()
    spz_prujezd = {}

    sql_query = (
        """
    SELECT SUM(ujete_km) AS celkem_km
    FROM Prujezd
    WHERE Vozidlo_SPZ = %s
    """
    )
    cursor.execute(sql_query, (spz,))
    celkem_km = cursor.fetchone()[0]
    spz_prujezd["celkem_km"] = celkem_km

    sql_query = (
        """
        SELECT Kredit FROM Vozidlo
        WHERE SPZ = %s
        """
    )
    cursor.execute(sql_query, (spz,))
    kredity = cursor.fetchone()[0]
    spz_prujezd["kredity"] = kredity

    sql_query = (
        """
        SELECT datum_prujezdu, brana_id, ujete_km FROM Prujezd
        WHERE Vozidlo_SPZ = %s
        """
    )
    cursor.execute(sql_query, (spz,))
    data = cursor.fetchall()
    data_dict = []

    for row in data:
        datum_prujezdu, brana_id, ujete_km = row
        prujezd_dict = {"datum_prujezdu": datum_prujezdu, 'brana_id': brana_id, 'ujete_km': ujete_km}
        data_dict.append(prujezd_dict)

    spz_prujezd["prujezd"] = data_dict
    closePostgreDb(conn, cursor)
    return spz_prujezd


def searchSPZ(spz):
    conn, cursor = connectToPostgreDb()

    cursor.execute("SELECT spz FROM Vozidlo")
    spz_records = cursor.fetchall()
    all_spz = [record[0] for record in spz_records]
    if spz in all_spz:
        spz_new = 0
    else:
        spz_new = 1

    closePostgreDb(conn, cursor)
    return spz_new

def updateKredits(spz, ujete_km):
    conn, cursor = connectToPostgreDb()

    sql_query = (
        """
        SELECT vozidlo.kredit, emisni_trida.sazba FROM vozidlo
        JOIN emisni_trida ON vozidlo.emisni_trida_typ = emisni_trida.typ
        WHERE vozidlo.spz = %s;
        """
    )
    cursor.execute(sql_query, (spz,))
    result = cursor.fetchone()
    kredit = result[0]
    sazba = result[1]

    sql_query = (
        """
        UPDATE Vozidlo
        SET Kredit = %s
        WHERE spz = %s;
        """
    )
    pay = ujete_km * sazba
    cursor.execute(sql_query, (kredit-pay, spz))
    conn.commit()
    closePostgreDb(conn, cursor)


def MongoToPostgre(collection):
    conn, cursor = connectToPostgreDb()
    for document in collection.find({}, {"brana_id": 1,
                                         "prujezd.datum_prujezdu": 1,
                                         "prujezd.registrace_vozidla.vozidlo.spz": 1,
                                         "prujezd.registrace_vozidla.vozidlo.emisni_trida": 1,
                                         "prujezd.registrace_vozidla.vozidlo.km_sazba": 1,
                                         "prujezd.registrace_vozidla.ujete_km": 1}):
        # print(document)
        brana_id = int(document["brana_id"])
        datum_prujezdu = int(document["prujezd"]["datum_prujezdu"])
        datum_prujezdu = datetime.fromtimestamp(datum_prujezdu)
        spz = document["prujezd"]["registrace_vozidla"]["vozidlo"]["spz"]
        emisni_trida = document["prujezd"]["registrace_vozidla"]["vozidlo"]["emisni_trida"]
        km_sazba = int(document["prujezd"]["registrace_vozidla"]["vozidlo"]["km_sazba"])
        ujete_km = int(document["prujezd"]["registrace_vozidla"]["ujete_km"])

        insert_stmt = (
            "INSERT INTO Emisni_trida (typ, sazba) VALUES (%s,%s) ON CONFLICT DO NOTHING"
        )
        data = (emisni_trida, km_sazba)
        cursor.execute(insert_stmt, data)

        spz_new = searchSPZ(spz)
        if spz_new == 1:
            kredit = random.randint(2000, 5000)
            insert_stmt = (
                "INSERT INTO Vozidlo (spz, kredit, emisni_trida_typ) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING"
            )
            data = (spz, kredit, emisni_trida)
            cursor.execute(insert_stmt, data)

        insert_stmt = (
            "INSERT INTO Prujezd (brana_id, datum_prujezdu, ujete_km, vozidlo_spz) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
        )
        data = (brana_id, datum_prujezdu, ujete_km, spz)
        cursor.execute(insert_stmt, data)

    conn.commit()
    closePostgreDb(conn, cursor)


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # zakomentovat po vytvřoení
    mydb = myclient["RDBsemestral"]
    mycol = mydb["TollGates"]
    # saveJsonToMongo('data/data-export2.json', mycol)
    # MongoToPostgre(mycol)
    # print(SPZ())
    # print(SPZ_Data('QQQ4567'))
    # print(searchSPZ('QQQ4567'))
