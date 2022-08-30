import pymysql as mysql

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

def modifyProductLike(sql_conn, args):
    vender = args.get('vender')
    pName = args.get('pName').strip()
    flag = args.get('flag') # like or unlike
    # pName='{pName}'
    sql_query = f"""
UPDATE productLike
SET `like`=`like`+({1 if flag == "like" else -1})
WHERE
	vender="{vender}" AND
	pName= (SELECT R.pName
				FROM (
						SELECT pName
						FROM productLike
						WHERE
							INSTR(pName, "{pName}")>0 AND INSTR(vender, "{vender}")>0
					) R
				);
    """

    sql_conn = SQLConnection(sql_conn, os.environ.get("DB_DB"))
    sql = sql_conn.cursor()

    sql.execute(sql_query)
    sql_conn.commit()

    res_code = 201

    sql_conn.close()

    return {'res_code': res_code}


