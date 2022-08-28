from flask import url_for

import os
from dotenv import load_dotenv

load_dotenv()

SPACE = "&nbsp;&nbsp;&nbsp;&nbsp;"
SERVER_IP = os.environ.get("SERVER_IP")

def make_link(links):
    ret_links = ""
    for link in links:
        ret_links += f"<a href='{link}'    target='_self' style='display:block'>{link}</a>"
    return ret_links

def make_form_query_table(link):
    form = f"<form action='{link}' method='GET'>\
        <p>판매점<input type='text' name='venders'> list: cu, gs25, emart24, seven_eleven, ministop ex)venders=cu,gs25 ex2)venders=emart24 </p>\
        <p>할인타입<input type='text' name='dtypes'> list: 1N1, 2N1, 3N1, GIFT, SALE ex)dtypes=1N1,2N1,SALE ex2)dtypes=SALE</p>\
        <p>상품이름<input type='text' name='products'> ex)products=옥수수 ex2)products=물</p>\
        <p>페이지 No.(1 이상)<input type='text' name='page'> ex)page=1 ex2)page=10</p>\
        <p><input type='submit' value='제출'></p>\
        </form>"
    return form

def make_html_body(args):
    body = []

    body.append("<h1>편의점 서버에서 바로 데이터 받아서 테이블로 출력</h1>")
    body.append(make_link(args['from_server']))
    body.append("<hr/>")
    body.append("<h1>데이터베이스에서 데이터 받아서 api 형태로 출력</h1>")
    body.append(make_link(args['from_db']))
    body.append("<hr/>")
    body.append("<h1>데이터베이스에서 데이터 받아서 테이블로 출력</h1>")
    body.append(make_link(args['from_db_make_table']))
    body.append("<hr/>")
    body.append("<h1>쿼리문 만들어서 가져오기(API)</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['from_db_select_query']} - GET</p>")
    body.append("<p>param: venders=&dtypes=&products=&page=</p>")
    body.append(params('query', args))
    body.append(return_value('query'))
    # body.append("<hr/>")
    # body.append("<h1>쿼리문 만들어서 가져오기(테이블 만들기)</h1>")
    # body.append(make_form_query_table(args['from_db_select_query_table']))
    body.append("<hr/>")
    body.append("<h1>쿼리로 입력한 값이 DB에 있는지 확인(API)</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['check_dup']} - GET</p>")
    body.append("<p>param: column=&data=</p>")
    body.append(params('dup', args))
    body.append(return_value('dup'))
    body.append("<hr/>")
    body.append("<h1>회원가입(API)</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['sign_up']} - POST</p>")
    body.append("<p>param: { </p>")
    body.append(f"<p>{SPACE}id: str, </p>")
    body.append(f"<p>{SPACE}pw: str, </p>")
    body.append(f"<p>{SPACE}name: str, </p>")
    body.append(f"<p>{SPACE}email: str, </p>")
    body.append("<p>} </p>")
    body.append(params('signup', args))
    body.append(return_value('signup'))


    return body

def return_value_query():
    data = [
        '{',
        f'{SPACE}response_code: int - 201: searched data exists, 202: searched data not exists',
        f'{SPACE}data: [',
        f'{SPACE}{SPACE}%s' % "{",
        f'{SPACE}{SPACE}{SPACE}vender: str,',
        f'{SPACE}{SPACE}{SPACE}dtype : str,',
        f'{SPACE}{SPACE}{SPACE}pName	: str,',
        f'{SPACE}{SPACE}{SPACE}pPrice: int,',
        f'{SPACE}{SPACE}{SPACE}pImg  : str,',
        f"{SPACE}{SPACE}%s, ..." % "}",
        f"{SPACE}]",
        "}",
    ]
    return data

def return_value_dup():
    data = [
        '{',
        f'{SPACE}res_code: int - 201: can craete this name/id, 202: cannot craete this name/id',
        f'{SPACE}{SPACE}{SPACE}{SPACE}{SPACE}{SPACE}400: cannot read properties, cause data value is \"\" or column value is \"\"',
        "}",
    ]
    return data

def return_value_signup():
    data = [
        '{',
        f'{SPACE}res_code: int - 201: append user to DB, 500: duplicate id/name in DB',
        "}",
    ]
    return data
    
def return_value(flag):
    ret = []
    ret.append('<button type="button" class="collapsible">return value</button>')
    ret.append('<div class="content">')

    if flag == "dup":
        data = return_value_dup()
    elif flag == "query":
        data = return_value_query()
    elif flag == "signup":
        data = return_value_signup()

    for dat in data:
        ret.append(f"<p>{dat}</p>")
    ret.append("</div>")

    return "".join(ret)


def params_query(link):
    form = f"<form action='{link}' method='GET'>\
        <p>venders=\
        <label><input type='checkbox' name='venders' value='cu'>cu</label>\
        <label><input type='checkbox' name='venders' value='gs25'>gs25</label>\
        <label><input type='checkbox' name='venders' value='seven_eleven'>seven_eleven</label>\
        <label><input type='checkbox' name='venders' value='emart24'>emart24</label>\
        <label><input type='checkbox' name='venders' value='ministop'>ministop</label>\
        <p>dtypes= \
        <label><input type='checkbox' name='dtypes' value='1N1'>1N1</label>\
        <label><input type='checkbox' name='dtypes' value='2N1'>2N1</label>\
        <label><input type='checkbox' name='dtypes' value='3N1'>3N1</label>\
        <label><input type='checkbox' name='dtypes' value='SALE'>SALE</label>\
        <label><input type='checkbox' name='dtypes' value='GIFT'>GIFT</label>\
        <p>products= <input type='text' name='products'> ex)products=옥수수 ex2)products=물</p>\
        <p>page= <input type='text' name='page'> ex)page=1 ex2)page=10, 1 이상의 값</p>\
        <p><input type='submit' value='제출'></p>\
        </form>"
    return form

def params_dup(link):
    form = f"""
        <form action='{link}' method='GET'>\
        <p>column=\
        <label><input type='radio' name='column' value='id' checked='checked'>id</label>\
        <label><input type='radio' name='column' value='name'>name</label>\
        <p>data= <input type='text' name='data'></p>\
        <p><input type='submit' value='제출'></p>\
        </form>
    """

    return form

def params_signup(link):
    form = f"<form action='{link}' method='POST'>\
        <p>id= <input type='text' name='id' id='id'> - max len: 20</p>\
        <p>pw= <input type='text' name='pw' id='pw'></p>\
        <p>name= <input type='text' name='name' id='name'> - max len: 20(kor: 10)</p>\
        <p>email= <input type='text' name='email' id='email'> - max len: 50</p>\
        <p><input type='submit' value='제출' onclick='doNothing()'></p>\
        </form>"

    return form


def params(flag, args):
    ret = []
    ret.append('<button type="button" class="collapsible">params</button>')
    ret.append('<div class="content">')

    if flag == "dup":
        data = params_dup(args['check_dup'])
    elif flag == "query":
        data = params_query(args['from_db_select_query'])
    elif flag == "signup":
        data = params_signup(args['sign_up'])

    ret.append(data)
    ret.append("</div>")

    return "".join(ret)

def make_html(body):
    html = "<!DOCTYPE HTML>"
    html += "<html>"
    html += "<head>"
    html += "<title>Flask app</title>"
    html += f"<link rel='stylesheet' type='text/css' href='{ url_for('static', filename='css.css') }'>"
    html += f"<script src='{ url_for('static', filename='func.js') }'></script>"
    html += '<script src="//code.jquery.com/jquery-3.3.1.min.js"></script>'
    html += "</head>"
    html += "<body>"
    html += "".join(body)
    html += "</body>"
    html += "</html>"

    return html