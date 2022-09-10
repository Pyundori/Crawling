import pymysql as mysql
import hashlib

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

def sqlSelect(sql_query):
    sql_conn = mysql
    sql_conn = SQLConnection(sql_conn, os.environ.get('DB_DB'))

    sql = sql_conn.cursor()

    sql.execute(sql_query)
    row = sql.fetchone()

    sql_conn.close()

    return row

def isValidToken(token):
    try:
        payload = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=[os.environ.get('JWT_ALGO')])
    except:
        return False

    sql_query = f"""SELECT `token` FROM `{os.environ.get('TABLE_USER')}` WHERE id=\'{payload['id']}\'"""
    token_db = sqlSelect(sql_query)

    return token.split(".")[-1] == token_db[0], payload

def getUserDat(args):
    token = args.get('token')

    valid, payload = isValidToken(token)
    if not valid:
        res = {
            'res_code': 400,
            'id': "",
            'name': "",
            'login': "",
        }
        return res

    id = payload.get('id')
    name = payload.get('name')
    login = payload.get('login')

    res = {
        'res_code': 201,
        'id': id,
        'name': name,
        'login': login,
    }

    return res

def sqlCommit(sql_query):
    sql_conn = mysql
    sql_conn = SQLConnection(sql_conn, os.environ.get('DB_DB'))

    sql = sql_conn.cursor()
    sql.execute(sql_query)

    sql_conn.commit()

    sql_conn.close()

def modifyUserDat(sql_conn, args): # put
    # 현재는 토큰의 id만으로 modify 가능하게 해놨음.
    # 비번을 모를때도 수정 가능해서 jwt injection 가능할 것으로 예상 <- id는 중복 확인으로 알아낼 수 있다.
    token = args.get('token')
    col = args.get('col')
    data = args.get('data')

    valid, payload = isValidToken(token)
    if not valid:
        return {"res_code": 500, "token": token} # invalid token

    if col != "pw" and col != "name":
        return {"res_code": 400, "token": token}

    if col == "pw":
        for _ in range(int(os.environ.get('SHA_REPEAT'))):
            data = hashlib.sha512(data.encode()).hexdigest()

    update_query = f"""UPDATE {os.environ.get('TABLE_USER')} SET {col}='{data}' WHERE `id`='{payload['id']}'""" + ";"
    sqlCommit(update_query)

    payload[col] = data
    token = jwt.encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm=os.environ.get('JWT_ALGO'))

    update_query = f"""UPDATE {os.environ.get('TABLE_USER')} SET token='{token.split(".")[-1]}' WHERE `id`='{payload['id']}'""" + ";"
    sqlCommit(update_query)

    return {"res_code": 201, "token": token}