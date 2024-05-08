from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = [
    {'id': 1, 'name': 'John', 'age': 30},
    {'id': 2, 'name': 'Alice', 'age': 25},
    {'id': 3, 'name': 'Bob', 'age': 35}
]

## Testovací
@app.route('/api/data')
def get_data():
    return jsonify(data)  # Corrected syntax

#Data o průjezdech na základě SPZ
@app.route('/api/data')
def get_data():
    return jsonify(data)  # Corrected syntax

if __name__ == '__main__':
    app.run(debug=True)
