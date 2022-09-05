
SPACE = "&nbsp;&nbsp;&nbsp;&nbsp;"

def return_value_query():
    data = [
        '{',
        f'{SPACE}response_code: int - 201: searched data exists, 202: searched data not exists',
        f'{SPACE}data_cnt: int - 쿼리의 전체 데이터 개수',
        f'{SPACE}data: [',
        f'{SPACE}{SPACE}%s' % "{",
        f'{SPACE}{SPACE}{SPACE}vender: str,',
        f'{SPACE}{SPACE}{SPACE}dType : str,',
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
        f'{SPACE}res_code: int - 201: can craete this name/id/email, 202: cannot craete this name/id/email',
        f'{SPACE}{SPACE}{SPACE}{SPACE}{SPACE}{SPACE}400: cannot read properties, cause data value is \"\" or column value is \"\"',
        "}",
    ]
    return data

def return_value_signup():
    data = [
        '{',
        f'{SPACE}res_code: int - 201: append user to DB, 500: duplicate id/name/email in DB',
        "}",
    ]
    return data

def return_value_signin():
    data = [
        '{',
        f'{SPACE}res_code: int - 500: No user with id in DB, 501: PW isn\'t correct',
        f'{SPACE}{SPACE}{SPACE}{SPACE}{SPACE}502: invalid token',
        f'{SPACE}{SPACE}{SPACE}{SPACE}{SPACE}201: login success, 202: valid token',
        f'{SPACE}token: "" - return when login failed, jwt_tolen - return when login success',
        "}",
    ]
    return data

def return_value_user_data():
    data = [
        '{',
        f'{SPACE}res_code: int - 201: token valid, 400: token invalid',
        f'{SPACE}id: str',
        f'{SPACE}name: str',
        "}",
    ]
    return data

def return_value_user_modify():
    data = [
        '{',
        f'{SPACE}res_code: int - 400: column value is not correct, 500: invalid token',
        f'{SPACE}{SPACE}{SPACE}{SPACE}{SPACE}201: modify succeed',
        f'{SPACE}data: token - if changed => changed token, else => origin token',
        "}",
    ]
    return data

def return_value_product_like():
    data = [
        '{',
        f'{SPACE}res_code: int - 201: change successful, 400: change failed',
        "}",
    ]
    return data

def return_value_product_like_ranking():
    data = [
        '{',
        f'{SPACE}&lt;vender&gt;&&lt;product_name&gt; &#123;: str , key를 &로 분해하여 사용',
        f'{SPACE}{SPACE}like: int',
        f'{SPACE}{SPACE}pImg: str',
        f'{SPACE}{SPACE}pPrice: int',
        f'{SPACE}{SPACE}pType: str',
        f'{SPACE}&#125;, ...',
        '}'
    ]
    return data

def return_value_sns_login():
    data = [
        '{',
        f"{SPACE}res_code: int,  201 - register successful, 202 - already exist",
        f"{SPACE}{SPACE}{SPACE}{SPACE}{SPACE}400 - sql error, 401 - not support sns login type",
        f"{SPACE}if res_code == 201 or 202 => token: str",
        f"{SPACE}else => msg: str",
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
    elif flag == "signin":
        data = return_value_signin()
    elif flag == "userdata":
        data = return_value_user_data()
    elif flag == "usermodify":
        data = return_value_user_modify()
    elif flag == "productlike":
        data = return_value_product_like()
    elif flag == "likeranking":
        data = return_value_product_like_ranking()
    elif flag == "kakaologin" or flag == "googlelogin":
        data = return_value_sns_login()

    for dat in data:
        ret.append(f"<p>{dat}</p>")
    ret.append("</div>")

    return "".join(ret)