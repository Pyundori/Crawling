import src
from flask import Flask, request
import pymysql as mysql

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

sql_conn = mysql

@app.route("/")
def main():

    args = {
        'from_server' : ["seven_eleven", "emart24", "cu", "gs25"], 
        'from_db' : ["seven_eleven/fromdb", "emart24/fromdb", "cu/fromdb", "gs25/fromdb"],
        'from_db_make_table' : ["seven_eleven/fromdb/table", "emart24/fromdb/table", "cu/fromdb/table", "gs25/fromdb/table"],
        'from_db_select_query' : "/api/product_query",
        'from_db_select_query_table' : "/api/product_query/table",
    }

    body = src.make_html_body(args)
    html = src.make_html(body)

    return f"""{html}"""

@app.route("/<vender>")
def get_all_datas_from_vender_page(vender):
    if vender == "gs25":
        datas = src.gs25_api(os.environ.get('URL_GS25'))
        # datas = src.GETRequestAPI_Gs25(src.PAGE_LIST["gs25"])
    elif vender == "seven_eleven":
        datas = src.se_api(os.environ.get('URL_SE'))
        # datas = src.POSTRequestAPI_SevenEleven(src.PAGE_LIST["seven_eleven"])
    elif vender == "cu":
        datas = src.cu_api(os.environ.get('URL_CU'))
        # datas = src.POSTRequestAPI_Cu(src.PAGE_LIST['cu'])
    elif vender == "emart24":
        datas = src.emart24_api(os.environ.get('URL_EMART24'))
        # datas = src.GETRequestAPI_Emart24(src.PAGE_LIST['emart24'])
        
    table = src.makeTable(datas)

    return "".join(table)
    
@app.route("/<vender>/fromdb")
def print_datas_from_db(vender):
    datas = src.GETVenderDataFromDB(sql_conn, vender)
    datas = list(datas)

    return datas

@app.route("/<vender>/fromdb/table")
def print_table_from_db(vender):
    datas = src.GETVenderDataFromDB(sql_conn, vender)
    datas = list(datas)

    table = src.makeTableFromDB(datas)

    return "".join(table)

@app.route("/to_db")
def toDB():
    src.toDatabase(sql_conn)
    return ""

@app.route("/api/product_query")
def test_query():
    datas = src.GETCustomProductQuery(sql_conn, request.args)
    return datas

@app.route("/api/product_query/table")
def test_query_table():
    table = src.GETCustomProductQuery_Table(sql_conn, request.args)
    return "".join(table)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)