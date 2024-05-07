from flask import Flask, jsonify, render_template

app = Flask(__name__)


## REST API MANAGEMENT
@app.route('/api/data')
def get_data():
    # Your logic to retrieve data from the database or elsewhere
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
