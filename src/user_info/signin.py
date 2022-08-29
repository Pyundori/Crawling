import hashlib
import pymysql as mysql

import jwt

import os
from dotenv import load_dotenv

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

def checkDuplicated(column, data):
    sql_conn = mysql
    sql_conn = SQLConnection(sql_conn, os.environ.get('DB_DB'))

    sql = sql_conn.cursor()

    sql_query = f"SELECT COUNT(*) FROM `{os.environ.get('TABLE_USER')}` WHERE `{column}`='{data}'"
    sql.execute(sql_query)
    cnt = sql.fetchone()[0]

    sql_conn.close()

    # 201 : 중복된 데이터 없음
    # 202 : 중복된 데이터 있음
    if cnt == 0:
        return 201
    return 202

def sqlSelect(sql_query):
    sql_conn = mysql
    sql_conn = SQLConnection(sql_conn, os.environ.get('DB_DB'))

    sql = sql_conn.cursor()

    sql.execute(sql_query)
    row = sql.fetchone()

    sql_conn.close()

    return row

    None

def createJWT(id, pw):
    payload = {
        'id': id,
        'pw': pw,
    }

    token = jwt.encode(payload, os.environ.get("JWT_SECRET_KEY"), algorithm="HS256")

    return token

def signIn(args):
    id = args.get('id')
    pw = args.get('pw')
    token = args.get('token')

    if token != "":
        token_val = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=["HS256"])
        
        sql_query = f"SELECT pw FROM `{os.environ.get('TABLE_USER')}` WHERE id=\'{token_val['id']}\'"
        row = sqlSelect(sql_query)

        if row == None:
            return {'res_code': 502, 'data': ""} # invalid token
        
        t = token_val['pw']
        for _ in range(int(os.environ.get("SHA_REPEAT"))):
            t = hashlib.sha512(t.encode()).hexdigest()
        
        if t != row[0]:
            return {'res_code': 502, 'data': ""} # invalid token

        return {'res_code': 202, 'data': token} # valid token
    
    if checkDuplicated('id', id) == 201:
        return {'res_code': 500, 'data': ""} # not in database

    t = pw

    for _ in range(int(os.environ.get("SHA_REPEAT"))):
        t = hashlib.sha512(t.encode()).hexdigest()

    sql_query = f"SELECT pw FROM `{os.environ.get('TABLE_USER')}` WHERE id='{id}'"
    row = sqlSelect(sql_query)

    """sql_conn = mysql
    sql_conn = SQLConnection(sql_conn, os.environ.get('DB_DB'))

    sql = sql_conn.cursor()


    sql.execute(sql_query)
    row = sql.fetchone()

    sql_conn.close() """


    if t != row[0]:
        return {'res_code': 501, 'data': ""} # password is not correct

    token = createJWT(id, pw)

    return {'res_code': 201, 'data': token} # login