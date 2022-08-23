import src
from flask import Flask, request
import pymysql as mysql

from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

sql_conn = mysql


def make_link(links):
    ret_links = ""
    for link in links:
        ret_links += f"<a href='{link}'    target='_self' style='display:block'>{link}</a>"
    return ret_links

def make_form(link):
    form = f"<form action='{link}' methos='post'>\
        <p>판매점<input type='text' name='venders'> list: cu, gs25, emart24, seven_eleven ex)cu,gs25 </p>\
        <p>할인타입<input type='text' name='dtypes'> list: 1N1, 2N1, 3N1, GIFT, SALE ex) 1N1,2N1,SALE</p>\
        <p>상품이름<input type='text' name='products'> ex)옥수수 ex2)물</p>\
        <p><input type='submit' value='제출'></p>\
        </form>"
    return form

@app.route("/")
def main():
    body = []

    from_server = ["seven_eleven", "emart24", "cu", "gs25"]
    from_db = ["seven_eleven/fromdb", "emart24/fromdb", "cu/fromdb", "gs25/fromdb"]
    from_db_make_table = ["seven_eleven/fromdb/table", "emart24/fromdb/table", "cu/fromdb/table", "gs25/fromdb/table"]
    from_db_select_query = ["test_sql_query"]
    from_db_select_query_table = ["test_sql_query/table"]

    body.append(make_link(from_server))
    body.append("<hr/>")
    body.append(make_link(from_db))
    body.append("<hr/>")
    body.append(make_link(from_db_make_table))
    body.append("<hr/>")
    body.append("<p>쿼리문 만들어서 가져오기(API)<p>")
    body.append(make_form('/test_sql_query'))
    body.append("<hr/>")
    body.append("<p>쿼리문 만들어서 가져오기(테이블 만들기)<p>")
    body.append(make_form('/test_sql_query/table'))



    html = "<!DOCTYPE HTML>"
    html += "<html>"
    html += "<head>"
    html += "<title>Flask app</title>"
    html += "</head>"
    html += "<body>"
    html += "".join(body)
    html += "</body>"
    html += "</html>"

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

@app.route("/test_sql_query")
def test_query():
    datas = src.GETCustomProductQuery(sql_conn, request.args)
    return datas

@app.route("/test_sql_query/table")
def test_query_table():
    table = src.GETCustomProductQuery_Table(sql_conn, request.args)

    return "".join(table)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)