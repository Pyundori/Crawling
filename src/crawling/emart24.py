import requests
from bs4 import BeautifulSoup as bs
import re

import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

import os
from dotenv import load_dotenv

load_dotenv()

def GETRequestAPI_Emart24(url):
    img_path = 'https://www.emart24.co.kr'

    datas = {}

    for cate in ['SALE', '1n1', '2n1', '3n1', 'X2']:

        params = {
            'productCategory': cate,
            'cpage': "1"
        }

        responses = requests.get(url, data=params, verify=False).text
        soup = bs(responses, 'html.parser')

        page_line = soup.select('.eventProduct .paging .bgNone')[-1]['href'].replace("'", "")
        page_line = re.findall(r'\(([^)]+)', page_line)

        tabs = {}

        try:
            page_num = page_line.pop(0)
        except:
            cate = cate.replace("n", "N").replace("X2", "GIFT")
            datas[cate] = tabs
            continue

        for idx in range(1, int(page_num)+1):
            params = {
                'productCategory': cate,
                'cpage': str(idx)
            }

            responses = requests.get(url, data=params, verify=False).text

            soup = bs(responses, 'html.parser')
            body = soup.select_one('.tabContArea ul.categoryListNew')

            for li in body.select('li'):
                gift = None
                product_name = li.select_one('.productDiv').text
                product_price = li.select_one('.price').text.split('\xa0')[0]
                product_price = int(re.sub('[,.]', '', product_price))
                product_img = img_path + li.select_one('.productImg img')['src']

                tabs[product_name] = {'price': product_price, 'img': product_img, 'gift': gift}

        cate = cate.replace("n", "N").replace("X2", "GIFT")
        datas[cate] = tabs

    return datas

if __name__ == "__main__":
    datas = GETRequestAPI_Emart24(os.environ.get("URL_EMART24"))

    for leg, products in datas.items():
        for product, data in products.items():
            print(product, data)