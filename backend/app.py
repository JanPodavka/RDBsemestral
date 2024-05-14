import datetime
import json
import time

import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS

from libs.lib_boilplate import exportdata
from main import SPZ_Data, SPZ, Platba, vypisPlatby, saveJsonToMongo, MongoToPostgre

app = Flask(__name__)
CORS(app)

spzdata = [
    {'id': 1, 'name': 'John', 'age': 30},
    {'id': 2, 'name': 'Alice', 'age': 25},
    {'id': 3, 'name': 'Bob', 'age': 35}
]


# Data o průjezdech na základě SPZ
@app.route('/api/dataPrujezd', methods=['GET'])
def get_tabledata():
    spz = request.args.get('spz')  # Get selected SPZ from query parameters
    if spz is None:
        return jsonify({"error": "SPZ parameter is missing"}), 400
    data = SPZ_Data(spz)
    tabledata = data['prujezd']
    return tabledata

@app.route('/api/dataPlatba', methods=['GET'])
def get_platbydata():
    spz = request.args.get('spz')  # Get selected SPZ from query parameters
    if spz is None:
        return jsonify({"error": "SPZ parameter is missing"}), 400
    print(spz)
    data = vypisPlatby(spz)
    #tabledata = data['prujezd']
    return data

@app.route('/api/generate', methods=['POST'])
def get_generated():
    data = request.json  # Get platba parameters
    num = int(data["num"])
    exportdata(num)
    time.sleep(3)
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # zakomentovat po vytvřoení
    mydb = myclient["RDBsemestral"]
    mycol = mydb["TollGates"]
    saveJsonToMongo("data-export2.json", mycol)
    MongoToPostgre(mycol)
    if num is None:
        return jsonify({"error": "SPZ parameter is missing"}), 400



@app.route('/api/dataSPZ')
def get_dataSPZ():
    data = SPZ()
    return jsonify(data['spz'])  # Corrected syntax



# Platba
@app.route('/api/karta', methods=['POST'])
def get_karta():
    platba = request.json  # Get platba parameters
    platba = platba["platba"]
    print(platba)
    if platba is None:
        return jsonify({"error": "parameter is missing"}), 400
    Platba(platba)
    return jsonify({"OK"}), 200
    #add

@app.route('/api/celkem_money', methods=['POST'])
def get_celkem_money():
    platba = request.json  # Get platba parameters
    platba = platba["platba"]
    print(platba)
    if platba is None:
        return jsonify({"error": "parameter is missing"}), 400
    Platba(platba)
    return jsonify({"OK"}), 200

@app.route('/api/celkem_km', methods=['POST'])
def get_celkem_km():
    platba = request.json  # Get platba parameters
    spz = platba["spz"]

    if platba is None:
        return jsonify({"error": "parameter is missing"}), 400
    return jsonify(), 200

if __name__ == '__main__':
    app.run(debug=True)
