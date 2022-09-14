import pymysql as mysql
import jwt
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

def snsLogin(id, name, email, login):
    sql_conn = mysql
    sql_conn = sql_conn.connect(
            host        = 'localhost',   # 루프백주소, 자기자신주소
            user        = os.environ.get('DB_USER'),        # DB ID      
            password    = os.environ.get('DB_PW'),    # 사용자가 지정한 비밀번호
            database    = os.environ.get("DB_DB"),
            charset     = 'utf8',
        )

    sql = sql_conn.cursor()

    pw = ""
    for _ in range(int(os.environ.get("SHA_REPEAT"))):
        pw = hashlib.sha512(pw.encode()).hexdigest()

    payload = {
        'id': id,
        'pw': pw,
        'name': name,
        'login': login,
    }

    token = jwt.encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm=os.environ.get('JWT_ALGO'))

    sql_query = f"""INSERT INTO `{os.environ.get("TABLE_USER")}`(`id`, `pw`, `name`, `token`, `type`) VALUES ('{id}', '{pw}', '{name}', '{token.split(".")[-1]}', '{login}') """

    try:
        sql.execute(sql_query)
        sql_conn.commit()
    except mysql.err.OperationalError:
        return {"res_code": 400, "msg": "sql error"}
    except:
        sql_query = f"""UPDATE `{os.environ.get("TABLE_USER")}` SET `name`='{name}', `token`="{token.split(".")[-1]}" WHERE `id`='{id}' AND `type`='{login}'"""
        sql.execute(sql_query)
        sql_conn.commit()
        # return {"res_code": 202, "token": token} # already registed
    finally:
        sql_conn.close()

    return {"res_code": 201, "token": token} # regist success