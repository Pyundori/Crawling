import src
from flask import Flask, request, Response, json, url_for
import pymysql as mysql

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

sql_conn = mysql

vender_api = {
    "gs25"          : {'api': src.gs25_api,       'path': 'URL_GS25'},
    "seven_eleven"  : {'api': src.se_api,         'path': 'URL_SE'},
    "cu"            : {'api': src.cu_api,         'path': 'URL_CU'},
    "emart24"       : {'api': src.emart24_api,    'path': 'URL_EMART24'},
    "ministop"      : {'api': src.ministop_api,   'path': 'URL_MINISTOP'}, 
}

@app.route("/")
def main():
    args = {
        'from_db_select_query'          : "/api/product_query",
        'from_db_select_query_table'    : "/api/product_query/table",
        'check_dup'                     : "/api/user/check_dup",
    }

    args['from_server'] = [ path for path in vender_api.keys() ]
    args['from_db'] = [ path+'/fromdb' for path in args['from_server'] ]
    args['from_db_make_table'] = [ path+'/table' for path in args['from_db'] ]

    body = src.make_html_body(args)
    html = src.make_html(body)

    return f"""{html}"""

@app.route("/<vender>")
def get_all_datas_from_vender_page(vender):
    datas = {}
    try:
        datas = vender_api[vender]['api'](os.environ.get(vender_api[vender]['path']))
    except:
        None
        
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

@app.route("/api/product_query", methods=["GET"])
def product_query():
    datas = src.GETCustomProductQuery(sql_conn, request.args)

    temp = [ {
        'vender': x[0],
        'dtype': x[1],
        'pName': x[2],
        'pPrice': x[3],
        'pImg': x[4],
    } for x in datas ]

    res_code = 201 if len(temp) > 0 else 202
    ret_data = {
        'data': temp,
        'response_code': res_code,
    }

    # return temp
    json_str = json.dumps(ret_data, ensure_ascii=False)
    response = Response(json_str, content_type="application/json; charset=utf-8" )
    return response

@app.route("/api/product_query/table")
def product_query_table():
    table = src.GETCustomProductQuery_Table(sql_conn, request.args)
    return "".join(table)

# get
# args
#   column: id or name
#   data: <str>
@app.route("/api/user/check_dup")
def verify_column():
    args = request.args.to_dict()
    if args['data'] == "" or args['column'] == "": 
        return {'res_code': 400}    # 해당 데이터 추출 불가능. id나 name이 ""인 경우는 없다.
                                    # column값도 ""인 경우는 없다.
    res_code = src.checkDuplicated(args['column'], args['data'])
    return {'res_code': res_code}

@app.route("/test")
def test():
    dtypes = ",".join(request.args.getlist('dtypes'))
    dtypes = dtypes.split(',') if (len(dtypes)!=0) else []

    venders = ",".join(request.args.getlist('venders'))
    venders = venders.split(',') if (len(venders)!=0) else []

    return {'dtypes': dtypes, 'venders': venders}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)