from src import *
import time
from dotenv import load_dotenv
import os

load_dotenv()

def SQLConnection(sql_conn):
    sql_conn = sql_conn.connect(
            host        = os.environ.get('DB_HOST'),   # 루프백주소, 자기자신주소
            user        = os.environ.get('DB_USER'),        # DB ID      
            password    = os.environ.get('DB_PW'),    # 사용자가 지정한 비밀번호
            database    = 'crawling',
            charset     = 'utf8',
            # cursorclass = sql.cursors.DictCursor #딕셔너리로 받기위한 커서
        )
    return sql_conn

def toDatabase(sql_conn):
    gs25 = gs25_api(os.environ.get("URL_GS25"))
    gs25 = makeSQLDatas(gs25, "gs25")

    cu = cu_api(os.environ.get("URL_CU"))
    cu = makeSQLDatas(cu, "cu")

    emart24 = emart24_api(os.environ.get("URL_EMART24"))
    emart24 = makeSQLDatas(emart24, "emart24")

    seven_eleven = se_api(os.environ.get("URL_SE"))
    seven_eleven = makeSQLDatas(seven_eleven, "seven_eleven") 

    datas = gs25 + cu + emart24 + seven_eleven
    pushDataToDB(sql_conn, datas)

def pushDataToDB(sql_conn, datas):
    sql_conn = SQLConnection(sql_conn)
    sql = sql_conn.cursor()

    sql_query = "TRUNCATE crawledData"
    sql.execute(sql_query)
    sql_conn.commit()

    sql_query = "INSERT INTO crawledData (vender, pType, pName, pPrice, pImg, gName, gPrice, gImg) VALUES "
    sql_data = []

    idx, turn = 1, 1
    for data in datas:
        if idx % 100 == 0:
            turn += 1

            sql.execute(sql_query + ", ".join(sql_data) + ";")
            sql_conn.commit()
            sql_data = []
            idx = 1
            
        sql_value = "("
        sql_value += ",".join([ f'"{x}"' for x in data ])
        sql_value += ")"

        sql_data.append(sql_value)
        idx += 1

    if len(sql_data) > 0:
        sql_query += ", ".join(sql_data) + ";"
        sql.execute(sql_query)
        sql_conn.commit()
    
    sql_conn.close()

def makeVenderSQLQuery(venders=[], dtypes=[], products=[]):
    # vender case:
    vender_list = []
    if len(venders) > 0:
        for vender in venders:
            vender_list.append(f"vender='{vender}'")

    vender_list_query = " OR ".join(vender_list)
    if len(vender_list_query) > 0:
        vender_list_query = " WHERE " + vender_list_query
    sql_query_vender = "SELECT * FROM crawledData" + vender_list_query

    # type case:
    dtype_list = []
    if len(dtypes) > 0:
        for dtype in dtypes:
            dtype_list.append(f"pType='{dtype}'")

    dtype_list_query = " OR ".join(dtype_list)
    if len(dtype_list_query) > 0:
        dtype_list_query = " WHERE " + dtype_list_query
    sql_query_dtype = f"SELECT * FROM ({sql_query_vender}) V" + dtype_list_query

    # product_name case:
    product_list = []
    if len(products) > 0:
        for product in products:
            product_list.append(f"INSTR(pName, '{product}')>0")

    product_list_query = " OR ".join(product_list)
    if len(product_list_query) > 0:
        product_list_query = " WHERE " + product_list_query

    sql_query = \
    f"SELECT \
    A.vender, A.pType, A.pPrice, A.pName, A.pImg, A.gName, A.gPrice, A.gImg \
    FROM ({sql_query_dtype}) A" + product_list_query

    return sql_query

def makeTableFromDB(datas):
    thead = initThead()
    tbody = initTbody()

    index = 1
    for data in datas:
        # for product_name, product_data in legend_datas.items():
        tbody.insert(-1, "<tr>")

        tbody.insert(-1, setTbodyTag("td", index))
        index += 1
        tbody.insert(-1, setTbodyTag("td", data[0]))
        tbody.insert(-1, setTbodyTag("td", data[1]))
        tbody.insert(-1, setTbodyTag("td", data[2]))

        tbody.insert(-1, setTbodyTag("td", data[3]))
        tbody.insert(-1, setTbodyTag("td", setImgTag(data[4])))

        if data[5] != "null":                
            tbody.insert(-1, setTbodyTag("td", data[5]))
            
            tbody.insert(-1, setTbodyTag("td", data[6]))
            tbody.insert(-1, setTbodyTag("td", setImgTag(data[7])))

        tbody.insert(-1, "</tr>")

    table = thead + tbody
    table.insert(0, "<table>")
    table.append("</table>")

    return table

def initThead():
    thead = []
    thead.append("<thead>")
    thead.append("<tr>")

    thead.append(setTbodyTag("td", "index"))
    thead.append(setTbodyTag("td", "vender"))
    thead.append(setTbodyTag("td", "type"))
    thead.append(setTbodyTag("td", "name"))
    thead.append(setTbodyTag("td", "price"))
    thead.append(setTbodyTag("td", "img"))
    thead.append(setTbodyTag("td", "gift_name"))
    thead.append(setTbodyTag("td", "gift_price"))
    thead.append(setTbodyTag("td", "gift_img"))

    thead.append("</tr>")
    thead.append("</thead>")

    return thead

def GETVenderDataFromDB(sql_conn, vender):
    sql_conn = SQLConnection(sql_conn)

    sql_query = f"SELECT vender as V, pType as T, pName, pPrice, pImg, gName, gPrice, gImg FROM crawledData where vender='{vender}'"
    #sql_query = makeVenderSQLQuery(vender)
    
    sql = sql_conn.cursor()
    sql.execute(sql_query)

    rows = sql.fetchall()

    sql_conn.close()

    return rows

def getQueryFromArgs(args):
    venders = args.get('venders').replace(" ", "")
    venders = venders.split(',') if (len(venders)!=0) else []

    dtypes = args.get('dtypes').replace(" ", "")
    dtypes = dtypes.split(',') if (len(dtypes)!=0) else []

    products = args.get('products').replace(" ", "")
    products = products.split(',') if (len(products)!=0) else []

    return venders, dtypes, products

def GETCustomProductQuery(sql_conn, args):
    sql_conn = SQLConnection(sql_conn)

    # venders, dtypes, products
    venders, dtypes, products = getQueryFromArgs(args)
    # venders = ["cu", ...]
    # dtypes = ["2N1", ...]
    # products = ["수염차", ...]
    sql_query = makeVenderSQLQuery(venders=venders, dtypes=dtypes, products=products)
    
    sql = sql_conn.cursor()
    sql.execute(sql_query)

    rows = sql.fetchall()

    sql_conn.close()

    return list(rows)


def GETCustomProductQuery_Table(sql_conn, args):
    datas = GETCustomProductQuery(sql_conn, args)

    return makeTableFromDB(datas)