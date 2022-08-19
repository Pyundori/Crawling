import src
import json
import requests
from flask import Flask
import pymysql as mysql

app = Flask(__name__)

sql_conn = mysql.connect(
            host        ='localhost',   # 루프백주소, 자기자신주소
            user        ='test',        # DB ID      
            password    ='mysql123',    # 사용자가 지정한 비밀번호
            database    ='crawling',
            charset     ='utf8',
            # cursorclass = sql.cursors.DictCursor #딕셔너리로 받기위한 커서
        )

PAGE_LIST = {
    'seven_eleven': 'https://www.7-eleven.co.kr/product/listMoreAjax.asp',
    'gs25': 'http://gs25.gsretail.com/gscvs/ko/products/event-goods-search',
    'emart24': 'https://www.emart24.co.kr/product/eventProduct.asp',
    'cu': 'https://cu.bgfretail.com/event/plusAjax.do',
}

@app.route("/")
def main():
    body = []
    # body.append("<div>")
    body.append("<a href='seven_eleven'    target='_self' style='display:block'>seven_eleven</a>")
    body.append("<a href='emart24'         target='_self' style='display:block'>emart24</a>")
    body.append("<a href='cu'              target='_self' style='display:block'>cu</a>")
    body.append("<a href='gs25'            target='_self' style='display:block'>gs25</a>")
    # body.append("</div>")

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

@app.route("/seven_eleven")
def seven_eleven():
    seven_eleven = src.POSTRequestAPI_SevenEleven(PAGE_LIST["seven_eleven"])
    table, datas = src.makeTable(seven_eleven)
    return "".join(table)

@app.route("/emart24")
def emart24():
    emart24 = src.GETRequestAPI_Emart24(PAGE_LIST['emart24'])
    table, datas = src.makeTable(emart24)
    return "".join(table)

@app.route("/cu")
def cu():
    cu = src.POSTRequestAPI_Cu(PAGE_LIST['cu'])
    table, datas = src.makeTable(cu)
    return "".join(table)

@app.route("/gs25")
def crawling():
    gs25 = src.GETRequestAPI_Gs25(PAGE_LIST["gs25"])
    table, datas = src.makeTable(gs25)

    src.pushDataToDB(sql_conn, datas)

    return "".join(table)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)