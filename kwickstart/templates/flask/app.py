from flask import Flask, jsonify, request

PORT = 5000
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/data')
def data():
    return jsonify({'error': False, 'data': 123})


if __name__ == "__main__":
    print('Running on http://127.0.0.1:' + str(PORT))
    app.run('0.0.0.0', PORT)
