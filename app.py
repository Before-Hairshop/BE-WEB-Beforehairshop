from flask import Flask
from flask import request
from flask import jsonify
import flask
import pymysql
from db_connection import connect_db
from db_connection import close_db
# from flask_api import status


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

# ==================
## 리뷰 생성 API
# ==================
@app.route('/reviews', methods=['POST'])
def create_review():
    param = request.get_json()

    ## AWS RDS 연결
    conn, cur = connect_db()

    ## insert data - review table
    insert_sql = "insert into review (user_id, content) values (%s, %s);"
    review_values = (param['user_id'], param['review'])
    
    cur.execute(insert_sql, review_values)
    conn.commit()

    ## AWS RDS 연결 해제
    close_db(conn, cur)

    response_result = { 'result' : 'success' }

    # print(param['review'])
    return jsonify(response_result), 201
