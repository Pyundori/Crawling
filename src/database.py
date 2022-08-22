from src import *
import time

def SQLConnection(sql_conn):
    sql_conn = sql_conn.connect(
            host        ='localhost',   # 루프백주소, 자기자신주소
            user        ='test',        # DB ID      
            password    ='mysql123',    # 사용자가 지정한 비밀번호
            database    ='crawling',
            charset     ='utf8',
            # cursorclass = sql.cursors.DictCursor #딕셔너리로 받기위한 커서
        )
    return sql_conn

def toDatabase(sql_conn):
    start = time.time()
    gs25 = GETRequestAPI_Gs25(PAGE_LIST["gs25"])
    gs25 = makeSQLDatas(gs25, "gs25")
    print('gs25 end', time.time() - start, len(gs25))

    start = time.time()
    cu = POSTRequestAPI_Cu(PAGE_LIST['cu'])
    cu = makeSQLDatas(cu, "cu")
    print('cu end', time.time() - start, len(cu))

    start = time.time()
    emart24 = GETRequestAPI_Emart24(PAGE_LIST['emart24'])
    emart24 = makeSQLDatas(emart24, "emart24")
    print('emart24 end', time.time() - start, len(emart24))

    start = time.time()
    seven_eleven = POSTRequestAPI_SevenEleven(PAGE_LIST["seven_eleven"])
    seven_eleven = makeSQLDatas(seven_eleven, "seven_eleven")
    print('seven_eleven end', time.time() - start, len(seven_eleven))

    start = time.time()
    datas = gs25 + cu + emart24 + seven_eleven
    pushDataToDB(sql_conn, datas)
    print('db end', time.time() - start, len(datas))

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

def makeVenderSQLQuery(vender):
    return f"SELECT vender as V, pType as T, pName, pPrice, pImg, gName, gPrice, gImg FROM crawledData WHERE vender='{vender}';"

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

def setTbodyTag(tag, dat):
    return f"<{tag}>{dat}</{tag}>"

def GETVenderDataFromDB(sql_conn, vender):
    sql_conn = SQLConnection(sql_conn)

    sql_query = makeVenderSQLQuery(vender)
    
    sql = sql_conn.cursor()
    sql.execute(sql_query)

    rows = sql.fetchall()

    sql_conn.close()

    return rows