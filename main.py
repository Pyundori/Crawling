import src
from flask import Flask
import pymysql as mysql
from flask import request

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
        datas = src.GETRequestAPI_Gs25(src.PAGE_LIST["gs25"])
    elif vender == "seven_eleven":
        datas = src.POSTRequestAPI_SevenEleven(src.PAGE_LIST["seven_eleven"])
    elif vender == "cu":
        datas = src.POSTRequestAPI_Cu(src.PAGE_LIST['cu'])
    elif vender == "emart24":
        datas = src.GETRequestAPI_Emart24(src.PAGE_LIST['emart24'])
        
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

def getQueryFromArgs(args):
    venders = args.get('venders').replace(" ", "")
    venders = venders.split(',') if (len(venders)!=0) else []

    dtypes = args.get('dtypes').replace(" ", "")
    dtypes = dtypes.split(',') if (len(dtypes)!=0) else []

    products = args.get('products').replace(" ", "")
    products = products.split(',') if (len(products)!=0) else []

    return venders, dtypes, products

@app.route("/test_sql_query")
def test_query():
    sql_conn = mysql.connect(
            host        ='localhost',   # 루프백주소, 자기자신주소
            user        ='test',        # DB ID      
            password    ='mysql123',    # 사용자가 지정한 비밀번호
            database    ='crawling',
            charset     ='utf8',
            # cursorclass = sql.cursors.DictCursor #딕셔너리로 받기위한 커서
        )

    # venders, dtypes, products
    venders, dtypes, products = getQueryFromArgs(request.args)
    # venders = ["cu", ...]
    # dtypes = ["2N1", ...]
    # products = ["수염차", ...]
    sql_query = src.makeVenderSQLQuery(venders=venders, dtypes=dtypes, products=products)
    
    sql = sql_conn.cursor()
    sql.execute(sql_query)

    rows = sql.fetchall()

    sql_conn.close()

    return list(rows)

@app.route("/test_sql_query/table")
def test_query_table():
    sql_conn = mysql.connect(
            host        ='localhost',   # 루프백주소, 자기자신주소
            user        ='test',        # DB ID      
            password    ='mysql123',    # 사용자가 지정한 비밀번호
            database    ='crawling',
            charset     ='utf8',
            # cursorclass = sql.cursors.DictCursor #딕셔너리로 받기위한 커서
        )

    # venders, dtypes, products
    venders, dtypes, products = getQueryFromArgs(request.args)
    # venders = ["cu", ...]
    # dtypes = ["2N1", ...]
    # products = ["수염차", ...]
    sql_query = src.makeVenderSQLQuery(venders=venders, dtypes=dtypes, products=products)
    
    sql = sql_conn.cursor()
    sql.execute(sql_query)

    rows = sql.fetchall()

    sql_conn.close()

    datas = list(rows)

    table = src.makeTableFromDB(datas)

    return "".join(table)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)