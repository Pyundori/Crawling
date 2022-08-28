import pymysql as mysql

import os
from dotenv import load_dotenv

load_dotenv()

def getUserDat():
    sql_conn = mysql
    sql_conn = SQLConnection(sql_conn, os.environ.get('DB_DB'))

    sql = sql_conn.cursor()

    sql_query = f"SELECT name, email FROM `{os.environ.get('TABLE_USER')}` WHERE `id`='{id}'"
    sql.execute(sql_query)
    try:
        row = sql.fetchone()
        name = row[0]
        email = row[1]
        res_code = 201 # 데이터 찾음
    except:
        name = ""
        email = ""
        res_code = 500 # 해당 유저 없음

    sql_conn.close()

    res = {
        'res_code': res_code,
        'name': name,
        'email': email,
    }
    return res

