import datetime

from flask import Flask, jsonify
from flask_cors import CORS

from main import SPZ_Data

app = Flask(__name__)
CORS(app)

data = [
    {'id': 1, 'name': 'John', 'age': 30},
    {'id': 2, 'name': 'Alice', 'age': 25},
    {'id': 3, 'name': 'Bob', 'age': 35}
]
data2 = {'celkem_km': 153, 'kredity': -942,
         'prujezd': [{'datum_prujezdu': datetime.datetime(2024, 5, 6, 15, 32, 41), 'brana_id': 1111, 'ujete_km': 10},
                     {'datum_prujezdu': datetime.datetime(2024, 5, 6, 15, 32, 41), 'brana_id': 0, 'ujete_km': 30},
                     {'datum_prujezdu': datetime.datetime(2024, 5, 6, 15, 32, 41), 'brana_id': 3333, 'ujete_km': 34},
                     {'datum_prujezdu': datetime.datetime(2024, 5, 6, 15, 32, 41), 'brana_id': 4444, 'ujete_km': 20},
                     {'datum_prujezdu': datetime.datetime(2024, 5, 6, 15, 32, 41), 'brana_id': 2222, 'ujete_km': 59}]}


## Testovací
@app.route('/api/data')
def get_data():
    return jsonify(data)  # Corrected syntax


# Data o průjezdech na základě SPZ
@app.route('/api/dataPrujezd')
def get_tabledata():
    data = SPZ_Data('QQQ4567')
    km = data['celkem_km']
    kredity = data['kredity']
    tabledata = data['prujezd']
    return jsonify(tabledata)  # Corrected syntax


if __name__ == '__main__':
    app.run(debug=True)
