def params_query(link):
    form = f"""<form action='{link}' method='GET'>
        <p>venders=
        <label><input type='checkbox' name='venders' value='cu'>cu</label>
        <label><input type='checkbox' name='venders' value='gs25'>gs25</label>
        <label><input type='checkbox' name='venders' value='seven_eleven'>seven_eleven</label>
        <label><input type='checkbox' name='venders' value='emart24'>emart24</label>
        <label><input type='checkbox' name='venders' value='ministop'>ministop</label>
          | type: str</p>
        <p>dtypes= 
        <label><input type='checkbox' name='dtypes' value='1N1'>1N1</label>
        <label><input type='checkbox' name='dtypes' value='2N1'>2N1</label>
        <label><input type='checkbox' name='dtypes' value='3N1'>3N1</label>
        <label><input type='checkbox' name='dtypes' value='SALE'>SALE</label>
        <label><input type='checkbox' name='dtypes' value='GIFT'>GIFT</label>
          | type: str</p>
        <p>products= <input type='text' name='products'>  | type: str</p>
        <p>page= <input type='text' name='page'>  | type: int, 1 이상의 값</p>
        <p><input type='submit' value='제출'></p>
        </form>"""
    return form

def params_dup(link):
    form = f"""
        <form action='{link}' method='GET'>
        <p>column=
        <label><input type='radio' name='column' value='id' checked='checked'>id</label>
        <label><input type='radio' name='column' value='name'>name</label>
        <label><input type='radio' name='column' value='email'>email</label>
          | type: str</p>
        <p>data= <input type='text' name='data'>  | type: str</p>
        <p><input type='submit' value='제출'></p>
        </form>"""

    return form

def params_signup(link):
    form = f"""<form action='{link}' method='POST'>
        <p>id= <input type='text' name='id'>  | type: str, max len: 20</p>
        <p>pw= <input type='text' name='pw'></p>
        <p>name= <input type='text' name='name'>  | type: str, max len: 20(kor: 10)</p>
        <p><input type='submit' value='제출'></p>
        </form>"""

    return form

def params_signin(link):
    form = f"""<form action='{link}' method='POST'>
        <p>id= <input type='text' name='id'>  | type: str</p>
        <p>pw= <input type='text' name='pw'>  | type: str</p>
        
        <p><input type='submit' value='제출'></p>
        </form>"""
    #<p>token= <input type='text' name='token'>  | type: str</p>
    return form
    
def params_user_data(link):
    form = f"""<form action='{link}' method='POST'>
        <p>token= <input type='text' name='token'>  | type: str</p>
        <p><input type='submit' value='제출'></p>
        </form>"""

    return form

def params_user_modify(link):
    form = f"""<form action='{link}' method='POST'>
        <p>token= <input type='text' name='token'>  | type: str</p>
        <p>col= <input type='text' name='col'>  | type: str, value: pw, email</p>
        <p>data= <input type='text' name='data'> | type: str</p>
        <p><input type='submit' value='제출'></p>
        </form>"""

    return form

def params_product_like(link):
    form = f"""<form action='{link}' method='POST'>
        <p>vender= <input type='text' name='vender'>  | type: str</p>
        <p>pName= <input type='text' name='pName'>  | type: str</p>
        <p>flag= <input type='text' name='flag'>  | type: str, value: like or else..</p>
        <p><input type='submit' value='제출'></p>
        </form>"""

    return form

def params_product_like_ranking(link):
    form = f"""<form action='{link}' method='GET'>
        <p><input type='submit' value='제출'></p>
        </form>"""

    return form

def params_sns_login(link):
    form = f"""<form action='{link}' method="POST">
        <p>token= <input type='text' name='token'> | type: str</p>
        <p><input type='submit' value='제출'></p>
        </form>"""

    return form

def params(flag, args, login=""):
    ret = []
    ret.append('<button type="button" class="collapsible">params</button>')
    ret.append('<div class="content">')

    if flag == "dup":
        data = params_dup(args['check_dup'])
    elif flag == "query":
        data = params_query(args['from_db_select_query'])
    elif flag == "signup":
        data = params_signup(args['sign_up'])
    elif flag == "signin":
        data = params_signin(args['sign_in'])
    elif flag == "userdata":
        data = params_user_data(args['get_user'])
    elif flag == "usermodify":
        data = params_user_modify(args['user_modify'])
    elif flag == "productlike":
        data = params_product_like(args['product_like'])
    elif flag == "likeranking":
        data = params_product_like_ranking(args['like_ranking'])
    elif flag == "kakaologin":
        data = params_sns_login(args['kakao_login'])
    elif flag == "googlelogin":
        data = params_sns_login(args['google_login'])

    ret.append(data)
    ret.append("</div>")

    return "".join(ret)