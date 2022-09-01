import requests
from bs4 import BeautifulSoup as bs
import json

import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

import os
from dotenv import load_dotenv

load_dotenv()

def GetGs25Token():
    responses = requests.get("http://gs25.gsretail.com/gscvs/ko/products/event-goods").text

    soup = bs(responses, 'html.parser')
    token = soup.select_one("#CSRFForm input")['value']

    return 'CSRFToken=' + token

def GETRequestAPI_Gs25(url):
    token = GetGs25Token()
    datas = {}
    # , "GIFT"
    for param in ['ONE_TO_ONE', 'TWO_TO_ONE', "GIFT"]:
        tabs = {}
        params = f'pageNum=1&pageSize=10000&searchType=&searchWord=&parameterList={param}'
        # api_url = url + ';' + params

        api_url = url + '?' + token + ';' + params

        responses = json.loads(requests.get(url=api_url).json())['results']
        for data in responses:
            gift = None
            product_name = data['goodsNm'].strip()
            product_img = data['attFileNm']
            product_price = data['price']
            if type(product_price) == float:
                product_price = int(product_price)
            elif type(product_price) == str:
                product_price = product_price.split(".")[0]

            if param == "GIFT":
                gift = {}
                try:
                    gift_name = data['giftGoodsNm'].strip()
                except:
                    gift_name = "null"

                try:
                    gift_img = data['giftAttFileNm']
                except:
                    gift_img = "null"

                try:
                    gift_price =  data['giftPrice']

                    if type(gift_price) == float:
                        gift_price = int(gift_price)
                    elif type(gift_price) == str:
                        gift_price = gift_price.split(".")[0]
                except:
                    gift_price = 0

                gift[gift_name] = {'price': gift_price, 'img': gift_img}
            
            tabs[product_name] = {'price': product_price, 'img': product_img, 'gift': gift}

        param = param.replace("ONE", "1").replace("TWO", "2").replace("THREE", "3").replace("_", "").replace("TO", "N")
        datas[param] = tabs
    return datas

if __name__ == "__main__":
    datas = GETRequestAPI_Gs25(os.environ.get("URL_GS25"))

    for leg, products in datas.items():
        for product, data in products.items():
            print(product, data)