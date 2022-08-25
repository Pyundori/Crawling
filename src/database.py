from src import *
import time
from dotenv import load_dotenv
import os

load_dotenv()

def SQLConnection(sql_conn):
    sql_conn = sql_conn.connect(
            host        = 'localhost',   # 루프백주소, 자기자신주소
            user        = os.environ.get('DB_USER'),        # DB ID      
            password    = os.environ.get('DB_PW'),    # 사용자가 지정한 비밀번호
            database    = 'crawling',
            charset     = 'utf8',
            # cursorclass = sql.cursors.DictCursor #딕셔너리로 받기위한 커서
        )
    return sql_conn

def makeSQLQuery(venders=[], dtypes=[], products=[], page=1):
    # 특정 개수만 가져옴
    MAX_CNT = 10
    LIMIT = f" LIMIT {MAX_CNT * (page-1)}, {MAX_CNT}"

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
    A.vender, A.pType, A.pName, A.pPrice, A.pImg, A.gName, A.gPrice, A.gImg \
    FROM ({sql_query_dtype}) A" + product_list_query + LIMIT

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
    #sql_query = makeSQLQuery(vender)
    
    sql = sql_conn.cursor()
    sql.execute(sql_query)

    rows = sql.fetchall()

    sql_conn.close()

    return rows

def getQueryFromArgs(args):
    try:
        venders = ",".join(args.getlist('venders'))
        # venders = args.get('venders').replace(" ", "")
        venders = venders.split(',') if (len(venders)!=0) else []
    except:
        venders = []

    try:
        dtypes = ",".join(args.getlist('dtypes'))
        # dtypes = args.get('dtypes').replace(" ", "")
        dtypes = dtypes.split(',') if (len(dtypes)!=0) else []
    except:
        dtypes = []

    try:
        products = args.get('products').replace(" ", "")
        products = products.split(',') if (len(products)!=0) else []
    except:
        products = []

    try:
        page = args.get('page')
        try:
            page = int(page)
        except:
            page = 1
    except:
        page = 1

    return venders, dtypes, products, page

def GETCustomProductQuery(sql_conn, args):
    sql_conn = SQLConnection(sql_conn)

    venders, dtypes, products, page = getQueryFromArgs(args)
    sql_query = makeSQLQuery(venders=venders, dtypes=dtypes, products=products, page=page)
    print(sql_query)
    
    sql = sql_conn.cursor()
    sql.execute(sql_query)

    rows = sql.fetchall()

    sql_conn.close()

    return list(rows)


def GETCustomProductQuery_Table(sql_conn, args):
    datas = GETCustomProductQuery(sql_conn, args)

    return makeTableFromDB(datas)