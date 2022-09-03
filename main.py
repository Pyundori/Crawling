import src
from flask import Flask, request, Response, json, render_template
import pymysql as mysql
import json

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

args = {}

def setArgs():   
    global args 
    args = {
        'from_db_select_query'          : "/api/product_query",
        'from_db_select_query_table'    : "/api/product_query/table",
        'check_dup'                     : "/api/user/check_dup",
        'sign_up'                       : "/api/user/signup",
        'sign_in'                       : "/api/user/signin",
        'get_user'                      : "/api/user/get",
        'user_modify'                   : "/api/user/modify",
        'product_like'                  : "/api/product/like",
        'like_ranking'                  : "/api/product/ranking",
        'sns_login'                     : "/api/register",
    }

    args['from_server'] = [ path for path in vender_api.keys() ]
    args['from_db'] = [ path+'/fromdb' for path in args['from_server'] ]
    args['from_db_make_table'] = [ path+'/table' for path in args['from_db'] ]

@app.route("/")
def main():
    body = src.make_html_body(args, vender_api)
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
        'dType': x[1],
        'pName': x[2],
        'pPrice': x[3],
        'pImg': x[4],
    } for x in datas['row'] ]

    res_code = 201 if len(temp) > 0 else 202
    ret_data = {
        'data': temp,
        'data_cnt': datas['cnt'],
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
@app.route("/api/user/check_dup", methods=["GET"])
def verify_column():
    args = request.args
    if args['data'] == "" or args['column'] == "": 
        return {'res_code': 400}    # 해당 데이터 추출 불가능. id나 name이 ""인 경우는 없다.
                                    # column값도 ""인 경우는 없다.
    res_code = src.checkDuplicated(args['column'], args['data'])
    return {'res_code': res_code}

# post
@app.route("/api/user/signup", methods=["POST"])
def sign_up():
    try:
        args = request.json
    except:
        args = request.form
    return src.signUp(args)


@app.route("/api/user/signin", methods=["POST"])
def sign_in():
    try:
        args = request.json
    except:
        args = request.form
    return src.signIn(args)

@app.route("/api/user/get", methods=["POST"])
def get_user(): # POST 이용하여 json으로 받아야할까?
    try:
        args = request.json
    except:
        args = request.form
    return src.getUserDat(args)
    None

@app.route("/api/user/modify", methods=["POST"])
def modify_user(): # POST 이용하여 json으로 받아야할까?
    # PUT 안된다. 그냥 POST로 하자
    try:
        args = request.json
    except:
        args = request.form
    return src.modifyUserDat(sql_conn, args)

@app.route("/api/product/like", methods=["POST"])
def product_like():
    try:
        args = request.json
    except:
        args = request.form

    return src.modifyProductLike(sql_conn, args) 

@app.route("/api/product/ranking", methods=["GET"])
def product_like_ranking():
    return src.getProductLikeList(sql_conn)

@app.route("/api/register/<login>", methods=["POST"])
def sns_login(login):
    sns_login_list = ["kakao", "google"]
    if login not in sns_login_list:
        return {"res_code": 401, "msg": "not support sns login type"}

    try:
        id, email = request.json.get('id'), request.json.get('email')
    except:
        id, email = request.form.get('id'), request.form.get('email')

    res_data = src.snsLogin(id, email, login)
    return res_data

@app.route("/kakao/oauth2/callback", methods=["GET", "POST"])
def kakao_auth():
    import requests

    token = request.json.get('token')
    url = 'https://kapi.kakao.com/v2/user/me'

    headers = {
        "Authorization": f"""Bearer {token}"""
    }
    res = requests.get(url, headers=headers).json()

    id, email = res['id'], res['kakao_account']['email']
    res_data = src.snsLogin(id, email, 'kakao')

    return res_data


if __name__ == '__main__':
    setArgs()
    app.run(host="0.0.0.0", port=5000, debug=True)