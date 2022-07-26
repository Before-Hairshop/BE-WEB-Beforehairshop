from flask import Flask
from flask import request
from flask import jsonify
import flask
import pymysql
from db_connection import connect_db
from db_connection import close_db
# from flask_api import status
from config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_REGION
import boto3
import logging
from botocore.exceptions import ClientError

app = Flask(__name__)

s3_client = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_ACCESS_KEY, region_name = AWS_S3_BUCKET_REGION)

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

@app.route('/upload', methods=['POST'])
def upload():
    # user 테이블에 튜플 insert
    user_id = '1'
    path = '/' + user_id + '/' + 'profile.jpeg'
    try:
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': AWS_S3_BUCKET_NAME,
                                                            'Key': path},
                                                    ExpiresIn=1000 * 60 * 3) # 3분
    except ClientError as e:
        logging.error(e)
        return None
    return response

@app.route('/download', methods=['POST'])
def download():
    path = '/1/profile.jpeg'
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': AWS_S3_BUCKET_NAME,
                                                            'Key': path},
                                                    ExpiresIn=1000 * 60 * 3) # 3분
    except ClientError as e:
        logging.error(e)
        return None
    return response

# FLASK_APP=app.py flask run