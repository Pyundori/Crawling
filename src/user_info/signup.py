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

def signUp():
    None

if __name__ == "__main__":
    print(checkDuplicated('id', 'asdf'))