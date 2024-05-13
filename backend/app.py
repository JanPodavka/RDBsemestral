import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

from main import SPZ_Data, SPZ, Platba

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

@app.route('/api/dataSPZ')
def get_dataSPZ():
    data = SPZ()
    return jsonify(data['spz'])  # Corrected syntax

@app.route('/api/dataSPZ')
def get_spz():
    data = SPZ()
    tabledata = data['spz']
    return jsonify(tabledata)  # Corrected syntax

# Platba
@app.route('/api/karta', methods=['GET'])
def get_tabledata():
    platba = request.args.get('platba')  # Get platba parameters
    if platba is None:
        return jsonify({"error": "SPZ parameter is missing"}), 400
    Platba(platba)



if __name__ == '__main__':
    app.run(debug=True)
