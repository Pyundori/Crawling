from flask import url_for
from .param_form import params
from .return_value import return_value

import os
from dotenv import load_dotenv

load_dotenv()

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
    body.append("<h1>쿼리문 만들어서 가져오기(API) - GET</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['from_db_select_query']}</p>")
    body.append(params('query', args))
    body.append(return_value('query'))
    body.append("<hr/>")
    body.append("<h1>상품 좋아요 변경(API) - POST</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['product_like']}</p>")
    body.append(params('productlike', args))
    body.append(return_value('productlike'))
    body.append("<hr/>")
    body.append("<h1>상품 좋아요 랭킹(API) - GET</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['like_ranking']}</p>")
    body.append(params('likeranking', args))
    body.append(return_value('likeranking'))
    body.append("<hr/>")
    body.append("<h1>쿼리로 입력한 유저 데이터가 DB에 있는지 확인(API) - GET</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['check_dup']}</p>")
    body.append(params('dup', args))
    body.append(return_value('dup'))
    body.append("<hr/>")
    body.append("<h1>회원가입(API) - POST</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['sign_up']}</p>")
    body.append(params('signup', args))
    body.append(return_value('signup'))
    body.append("<hr/>")
    body.append("<h1>로그인(API) - POST</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['sign_in']}</p>")
    body.append(params('signin', args))
    body.append(return_value('signin'))
    body.append("<hr/>")
    body.append("<h1>SNS 로그인 - 자체 토큰 발행(API) - POST</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000/api/register/&lt;login&gt;</p>")
    body.append("<p>html상에서는 폼 구현 불가. REST 사용하여 요청.</p>")
    body.append("<p>현재 &lt;login&gt; 지원: kakao, google</p>")
    body.append(params('snslogin', args))
    body.append(return_value('snslogin'))
    body.append("<hr/>")
    body.append("<h1>유저 데이터 획득(API) - POST</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['get_user']}</p>")
    body.append(params('userdata', args))
    body.append(return_value('userdata'))
    body.append("<hr/>")
    body.append("<h1>유저 데이터 변경(API) - POST</h1>")
    body.append(f"<p>api_url: http://{SERVER_IP}:5000{args['user_modify']}</p>")
    body.append(params('usermodify', args))
    body.append(return_value('usermodify'))

    return body

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