import json
import pymongo
import psycopg2
from datetime import datetime
import random
#from pyliquibase import liquibase


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


#vypis vsech SPZ
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


#vypis dat pro konkretni SPZ
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


#hleda, zda konkretni SPZ je v databazi
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


#hleda, zda konkretni prujezd je v databazi
def searchPruj(spz, brana_id, datum_prujezdu):
    conn, cursor = connectToPostgreDb()

    sql_query = (
        """
    SELECT brana_id, datum_prujezdu
    FROM Prujezd
    WHERE Vozidlo_SPZ = %s
    """
    )
    cursor.execute(sql_query, (spz,))
    pru_records = cursor.fetchall()
    brana = [record[0] for record in pru_records]
    datum = [record[1] for record in pru_records]

    closePostgreDb(conn, cursor)

    for i, x in enumerate(brana):
        if brana[i] == brana_id and datum[i] == datum_prujezdu:
            return 0
        else:
            continue

    return 1


#zaplaceni kreditu pri prujezdu
def payKredit(spz, ujete_km):
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
        conn.commit()

        spz_new = searchSPZ(spz)
        if spz_new == 1:
            kredit = random.randint(2000, 5000)
            insert_stmt = (
                "INSERT INTO Vozidlo (spz, kredit, emisni_trida_typ) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING"
            )
            data = (spz, kredit, emisni_trida)
            cursor.execute(insert_stmt, data)
            conn.commit()

        pruj_new = searchPruj(spz, brana_id, datum_prujezdu)

        if pruj_new == 1:
            insert_stmt = (
                "INSERT INTO Prujezd (brana_id, datum_prujezdu, ujete_km, vozidlo_spz) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
            )
            data = (brana_id, datum_prujezdu, ujete_km, spz)
            cursor.execute(insert_stmt, data)
            payKredit(spz, ujete_km)
            conn.commit()

    closePostgreDb(conn, cursor)


#nahrani kreditu
def addKredit(spz, castka):
    conn, cursor = connectToPostgreDb()

    sql_query = (
        """
        SELECT kredit FROM vozidlo
        WHERE vozidlo.spz = %s;
        """
    )
    cursor.execute(sql_query, (spz,))
    kredit = cursor.fetchone()[0]

    sql_query = (
        """
        UPDATE Vozidlo
        SET Kredit = %s
        WHERE spz = %s;
        """
    )
    cursor.execute(sql_query, (kredit + castka, spz))
    conn.commit()
    closePostgreDb(conn, cursor)


#Platba pro nahrani kreditu
def Platba(data):
    typ = data["typ"]
    spz = data["spz"]
    data_platba = data["data"]
    if typ == "Karta":
        Karta(spz,data_platba)
    elif typ == "Hotovost":
        conn, cursor = connectToPostgreDb()
        castka = data_platba["Hotovost_castka"]
        datum_platby = datetime.fromtimestamp(data_platba["datum_platby"])


        insert_stmt = (
            "INSERT INTO Platba (spz, hotovost_castka, datum_platby) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING"
        )
        data = (spz, castka, datum_platby)
        cursor.execute(insert_stmt, data)
        conn.commit()

        addKredit(spz, castka)

        closePostgreDb(conn, cursor)
    elif typ == "Prevod":
        Prevod(spz, data_platba)


def Karta(spz, data_platba):
    conn, cursor = connectToPostgreDb()
    cislo_karty = int(data_platba["cislo_karty"])
    platnost = datetime.fromtimestamp(data_platba["platnost"])
    vlastnik = data_platba["vlastnik"]
    castka = int(data_platba["castka"])
    datum_platby = datetime.fromtimestamp(data_platba["datum_platby"])

    insert_stmt = (
        "INSERT INTO Karta (cislo_karty, platnost, vlastnik, castka) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    )
    data = (cislo_karty, platnost, vlastnik, castka)
    cursor.execute(insert_stmt, data)
    conn.commit()

    insert_stmt = (
        "INSERT INTO Platba (vozidlo_spz, Karta_cislo_karty, datum_platby) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING"
    )
    data = (spz, cislo_karty,datum_platby)
    cursor.execute(insert_stmt, data)
    conn.commit()

    addKredit(spz, castka)

    closePostgreDb(conn, cursor)


def Prevod(spz, data_platba):
    conn, cursor = connectToPostgreDb()
    cislo_uctu = data_platba["cislo_uctu"]
    vlastnik = data_platba["vlastnik"]
    castka = data_platba["castka"]
    datum_platby = datetime.fromtimestamp(data_platba["datum_platby"])

    insert_stmt = (
        "INSERT INTO Prevod (cislo_ucstu, vlastnik, castka) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING"
    )
    data = (cislo_uctu, vlastnik, castka)
    cursor.execute(insert_stmt, data)
    conn.commit()

    insert_stmt = (
        "INSERT INTO Platba (spz, Prevod_cislo_uctu, Datum_platby) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING"
    )
    data = (spz, cislo_uctu, datum_platby)
    cursor.execute(insert_stmt, data)
    conn.commit()

    addKredit(spz, castka)

    closePostgreDb(conn, cursor)


def vypisPlatby(spz):
    conn, cursor = connectToPostgreDb()
    sql_query = (
        """
        SELECT * FROM platba
        WHERE Vozidlo_spz = %s 
        """
    )
    cursor.execute(sql_query, (spz,))
    platba_records = cursor.fetchall()
    all_platba = [record for record in platba_records]
    closePostgreDb(conn, cursor)
    return(all_platba)


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # zakomentovat po vytvřoení
    mydb = myclient["RDBsemestral"]
    mycol = mydb["TollGates"]
    # saveJsonToMongo('data/data-export2.json', mycol)
    # MongoToPostgre(mycol)
    # print(SPZ())
    # print(SPZ_Data('QQQ4567'))
    # print(searchSPZ('QQQ4567'))
    # print(searchPruj('QQQ4567', 1111, datetime.fromtimestamp(1715002361)))
    #addKredit('QQQ4567',4000)
    #Platba({"typ":"Karta", "spz":"QQQ4567", "data":{"cislo_karty":"68","platnost":1715002361, "datum_platby":1715002361,"vlastnik":"Ondra","castka":5000}})
    print(vypisPlatby('QQQ4567'))