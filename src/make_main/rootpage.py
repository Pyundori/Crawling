def make_link(links):
    ret_links = ""
    for link in links:
        ret_links += f"<a href='{link}'    target='_self' style='display:block'>{link}</a>"
    return ret_links

def make_form(link):
    form = f"<form action='{link}' method='GET'>\
        <p>판매점<input type='text' name='venders'> list: cu, gs25, emart24, seven_eleven ex)venders=cu,gs25 ex2)venders=emart24 </p>\
        <p>할인타입<input type='text' name='dtypes'> list: 1N1, 2N1, 3N1, GIFT, SALE ex)dtypes=1N1,2N1,SALE ex2)dtypes=SALE</p>\
        <p>상품이름<input type='text' name='products'> ex)products=옥수수 ex2)products=물</p>\
        <p>페이지 No.(1 이상)<input type='text' name='page'> ex)page=1 ex2)page=10</p>\
        <p><input type='submit' value='제출'></p>\
        </form>"
    return form

def make_form_check():
    form = f"<form action='/api/product_query' method='GET'>\
        <p>venders=\
        <label><input type='checkbox' name='venders' value='cu'>cu</label>\
        <label><input type='checkbox' name='venders' value='gs25'>gs25</label>\
        <label><input type='checkbox' name='venders' value='seven_eleven'>seven_eleven</label>\
        <label><input type='checkbox' name='venders' value='emart24'>emart24</label>\
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

def make_html_body(args):
    body = []

    body.append(make_link(args['from_server']))
    body.append("<hr/>")
    body.append(make_link(args['from_db']))
    body.append("<hr/>")
    body.append(make_link(args['from_db_make_table']))
    body.append("<hr/>")
    body.append("<p>쿼리문 만들어서 가져오기(API)<p>")
    body.append("<p>param: venders=&dtypes=&products=&page=<p>")
    body.append(make_form(args['from_db_select_query']))
    body.append("<hr/>")
    body.append("<p>쿼리문 만들어서 가져오기(테이블 만들기)<p>")
    body.append(make_form(args['from_db_select_query_table']))
    body.append("<hr/>")
    body.append("<p>쿼리문 만들어서 가져오기(API) - 체크버튼을 이용하여 가시성 증가<p>")
    body.append("<p>param: venders=&dtypes=&products=&page=<p>")
    body.append(make_form_check())

    return body

def make_html(body):
    html = "<!DOCTYPE HTML>"
    html += "<html>"
    html += "<head>"
    html += "<title>Flask app</title>"
    html += "</head>"
    html += "<body>"
    html += "".join(body)
    html += "</body>"
    html += "</html>"

    return html