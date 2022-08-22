import src
from flask import Flask
import pymysql as mysql

app = Flask(__name__)

sql_conn = mysql


@app.route("/")
def main():
    body = []
    body.append("<a href='seven_eleven'    target='_self' style='display:block'>seven_eleven</a>")
    body.append("<a href='emart24'         target='_self' style='display:block'>emart24</a>")
    body.append("<a href='cu'              target='_self' style='display:block'>cu</a>")
    body.append("<a href='gs25'            target='_self' style='display:block'>gs25</a>")
    body.append("<hr/>")
    body.append("<a href='seven_eleven/fromdb'  target='_self' style='display:block'>seven_eleven_from_db</a>")
    body.append("<a href='emart24/fromdb'       target='_self' style='display:block'>emart24_from_db</a>")
    body.append("<a href='cu/fromdb'            target='_self' style='display:block'>cu_from_db</a>")
    body.append("<a href='gs25/fromdb'          target='_self' style='display:block'>gs25_from_db</a>")
    body.append("<hr/>")
    body.append("<a href='seven_eleven/fromdb/table'  target='_self' style='display:block'>seven_eleven_from_db_table</a>")
    body.append("<a href='emart24/fromdb/table'       target='_self' style='display:block'>emart24_from_db_table</a>")
    body.append("<a href='cu/fromdb/table'            target='_self' style='display:block'>cu_from_db_table</a>")
    body.append("<a href='gs25/fromdb/table'          target='_self' style='display:block'>gs25_from_db_table</a>")

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

# @app.route("/seven_eleven")
# def seven_eleven():
#     seven_eleven = src.POSTRequestAPI_SevenEleven(src.PAGE_LIST["seven_eleven"])
#     table = src.makeTable(seven_eleven)

#     return "".join(table)

# @app.route("/emart24")
# def emart24():
#     emart24 = src.GETRequestAPI_Emart24(src.PAGE_LIST['emart24'])
#     table = src.makeTable(emart24)

#     return "".join(table)

# @app.route("/cu")
# def cu():
#     cu = src.POSTRequestAPI_Cu(src.PAGE_LIST['cu'])
#     table = src.makeTable(cu)

#     return "".join(table)

# @app.route("/gs25")
# def gs25():
#     gs25 = src.GETRequestAPI_Gs25(src.PAGE_LIST["gs25"])
#     table = src.makeTable(gs25)

#     return "".join(table)

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

@app.route("/to_db") # 테스트 필요
def toDB():
    src.toDatabase(sql_conn)

    return ""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)