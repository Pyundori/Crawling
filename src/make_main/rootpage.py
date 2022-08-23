def make_link(links):
    ret_links = ""
    for link in links:
        ret_links += f"<a href='{link}'    target='_self' style='display:block'>{link}</a>"
    return ret_links

def make_form(link):
    form = f"<form action='{link}' methos='post'>\
        <p>판매점<input type='text' name='venders'> list: cu, gs25, emart24, seven_eleven ex)cu,gs25 </p>\
        <p>할인타입<input type='text' name='dtypes'> list: 1N1, 2N1, 3N1, GIFT, SALE ex) 1N1,2N1,SALE</p>\
        <p>상품이름<input type='text' name='products'> ex)옥수수 ex2)물</p>\
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
    body.append(make_form(args['from_db_select_query']))
    body.append("<hr/>")
    body.append("<p>쿼리문 만들어서 가져오기(테이블 만들기)<p>")
    body.append(make_form(args['from_db_select_query_table']))

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