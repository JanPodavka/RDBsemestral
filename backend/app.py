import datetime

from flask import Flask, jsonify
from flask_cors import CORS

from main import SPZ_Data, SPZ

app = Flask(__name__)
CORS(app)

spzdata = [
    {'id': 1, 'name': 'John', 'age': 30},
    {'id': 2, 'name': 'Alice', 'age': 25},
    {'id': 3, 'name': 'Bob', 'age': 35}
]



# Data o průjezdech na základě SPZ
@app.route('/api/dataPrujezd')
def get_tabledata():
    data = SPZ_Data('QQQ4567')
    km = data['celkem_km']
    kredity = data['kredity']
    tabledata = data['prujezd']
    return jsonify(tabledata)  # Corrected syntax

@app.route('/api/dataSPZ')
def get_spz():
    data = SPZ()
    tabledata = data['spz']
    return jsonify(tabledata)  # Corrected syntax


if __name__ == '__main__':
    app.run(debug=True)
