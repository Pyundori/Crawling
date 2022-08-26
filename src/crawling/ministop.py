import requests
import time
import math
from urllib import parse

url = 'https://www.ministop.co.kr/MiniStopHomePage/page/querySimple.do'

def POSTRequestAPI_Ministop(url):

    params = {
        'pageId': '',
        'sqlnum': 1,
        'paramInfo': '',
        'pageNum': 0,
        'sortGu': '',
        'tm': '',
    }


    legend = {
        'plus1': '1N1',
        'plus2': '2N1',
        'add': 'GIFT',
        'sale': 'SALE',
    }

    datas = {}
    img_path = "https://www.ministop.co.kr/MiniStopHomePage/page/pic.do"

    for idx, leg in enumerate(legend.items()):
        l = [1]
        tabs = {}
        print(idx, parse.quote(f"{idx+1}::"))
        for x in l:
            params['pageId'] = f'event/{leg[0]}'
            params['paramInfo'] = str(parse.quote(f"{idx+1}::"))
            params['pageNum'] = x
            params['tm'] = math.floor(time.time()*1000)

            res = requests.post(
                url=url,
                params="&".join([ f"{key}={val}" for key, val in params.items() ]),
            )
            
            for product in res.json()['recordList']:
                product = product['fields']
                tabs[product[-5]] = {'price': int(product[-4]), 'img': img_path + f"?n=event{leg[0]}." + product[-1]}
            
            l.append(x+1)

            if res.json()['havingMore'] == False:
                break
        datas[leg[1]] = tabs
    return datas