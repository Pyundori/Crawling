import PyMySql as mysql

import os
from dotenv import load_dotenv

load_dotenv()

def run():
    sql_conn = mysql
    truncateTable(sql_conn)

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

def truncateTable(sql_conn):
    sql_conn = SQLConnection(sql_conn, os.environ.get('DB_DB'))
    sql = sql_conn.cursor()

    sql_query = f"TRUNCATE TABLE {os.environ.get('TABLE_LIKE')}"
    sql.execute(sql_query)
    sql_conn.commit()

# crontab -e > 0 19 1 * * <python_path> <source_code_path>