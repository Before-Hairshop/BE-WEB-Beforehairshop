from secret import DB_PASSWORD, DB_USER, DB_HOST, DB_DATABASE
import pymysql

def connect_db():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER,
                         password=DB_PASSWORD, db=DB_DATABASE, port=3306)
    
    curs = conn.cursor(pymysql.cursors.DictCursor)
    return conn, curs

def close_db(conn, cur):
    cur.close()
    conn.close()