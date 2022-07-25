from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/reviews', methods=['POST'])
def create_review():
    param = request.get_json()
    print(param['review'])
    return param['review']
