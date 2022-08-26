import requests
import time
import math
from urllib import parse

import os
from dotenv import load_dotenv

load_dotenv()

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
    img_path = "https://www.ministop.co.kr/MiniStopHomePage/page/pic.do?n=event"

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
                gift = {}
                product = product['fields']
                if leg[0] == 'add':
                    img = img_path + f"{product[6].split(']')[1].split('_')[0]}.{product[6]}"
                    gift[product[3].split(" ")[0]] = {'price': int(product[4]), 'img': img}
                    img = img_path + f"{product[5].split(']')[1].split('_')[0]}.{product[5]}"
                    tabs[product[1]] = {'price': int(product[2]), 'img': img, 'gift': gift}

                else:    
                    img = img_path + f"{product[-1].split(']')[1].split('_')[0]}.{product[-1]}"
                    tabs[product[-5]] = {'price': int(product[-4]), 'img': img, 'gift': gift}
            
            l.append(x+1)

            if res.json()['havingMore'] == False:
                break
        datas[leg[1]] = tabs
    return datas

if __name__ == "__main__":
    datas = POSTRequestAPI_Ministop(os.environ.get("URL_MINISTOP"))

    for leg, products in datas.items():
        for product, data in products.items():
            print(product, data)