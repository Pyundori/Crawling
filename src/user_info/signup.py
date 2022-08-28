import hashlib
import pymysql as mysql

import os
from dotenv import load_dotenv

load_dotenv()

encoded_string = 'a'.encode()
hexdigest = hashlib.sha512(encoded_string).hexdigest()
print('a:', hexdigest, len(hexdigest))

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

def signUp(args):
    id = args.get('id')
    pw = args.get('pw')
    name = args.get('name')
    email = args.get('email')
    
    if checkDuplicated('id', id) == 202 or checkDuplicated('name', name) == 202:
        return {'res_code': 500} # same data in db, insert error

    for _ in range(int(os.environ.get("SHA_REPEAT"))):
        pw = hashlib.sha512(pw.encode()).hexdigest()

    sql_conn = mysql
    sql_conn = SQLConnection(sql_conn, os.environ.get('DB_DB'))

    sql = sql_conn.cursor()

    sql_query = f"INSERT INTO `{os.environ.get('TABLE_USER')}`(id, pw, name, email) VALUES ('{id}', '{pw}', '{name}', '{email}')"

    sql.execute(sql_query)
    sql_conn.commit()

    sql_conn.close()

    return {'res_code': 201} # data insert success

if __name__ == "__main__":
    print(checkDuplicated('id', 'asdf'))