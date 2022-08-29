import pymysql as mysql

import os
from dotenv import load_dotenv

import jwt

load_dotenv()

def SQLConnection(sql_conn, database):
    sql_conn = sql_conn.connect(
            host        = 'localhost',   # 루프백주소, 자기자신주소
            user        = os.environ.get('DB_USER'),        # DB ID      
            password    = os.environ.get('DB_PW'),    # 사용자가 지정한 비밀번호
            database    = database,
            charset     = 'utf8',
            # cursorclass = sql.cursors.DictCursor #딕셔너리로 받기위한 커서
        )
    return sql_conn

def getUserDat(args):
    token = args.get('token')

    token_val = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=[os.environ.get('JWT_ALGO')])
    id = token_val.get('id')

    sql_conn = mysql
    sql_conn = SQLConnection(sql_conn, os.environ.get('DB_DB'))

    sql = sql_conn.cursor()

    sql_query = f"SELECT name, email FROM `{os.environ.get('TABLE_USER')}` WHERE `id`='{id}'"
    sql.execute(sql_query)

    row = sql.fetchone()

    sql_conn.close()
    try:
        name = row[0]
        email = row[1]
        res_code = 201 # 데이터 찾음
    except:
        name = ""
        email = ""
        res_code = 500 # 해당 유저 없음

    res = {
        'res_code': res_code,
        'name': name,
        'email': email,
    }
    return res

def modifyDat(args):
    token = args.get('token')
    col = args.get('col')
    data = args.get('data')

    
