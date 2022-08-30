import requests
from bs4 import BeautifulSoup as bs
import re

import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

import os
from dotenv import load_dotenv

load_dotenv()

def GetCuSearchConditionLegend():
    url = 'https://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N'
    responses = requests.get(url).text

    soup = bs(responses, 'html.parser')
    searchConditions = soup.select_one("#contents .depth3Lnb .eventInfo")
    searchConditions = searchConditions.select('li')

    searchConditions = [ x.select_one('a') for x in searchConditions]
    searchConditions = { x['href']: x.text for x in searchConditions }
    searchConditions = { re.findall(r'\(([^)]+)', cond).pop(0).replace("'", ""): legend for cond, legend in searchConditions.items() }
    searchConditions = { cond: legend.replace("+", "N") for cond, legend in searchConditions.items() if len(cond) > 0 }

    return searchConditions

def POSTRequestAPI_Cu(url):
    datas = {}
    for cond, legend in GetCuSearchConditionLegend().items():
        idx = 1

        tabs = {}
        while True:
            responses = requests.post(url, verify=False, data={
                'pageIndex': idx,
                'listType': 0 if idx == 1 else 1,
                'searchCondition': cond, # "": all, "23": 1+1, "24": 2+1
                'user_id': ""
            }).text
            
            soup = bs(responses, 'html.parser')

            try:
                ul = soup.select_one('ul')
                _ = ul.select('li')[0]
            except:
                break

            for li in ul.select('li'):
                gift = None
                product_name = li.select_one('.prod_text .name p').text.strip()
                product_price = li.select_one('.prod_text .price strong').text.replace(",", "")
                product_price = int(product_price)
                product_img = li.select_one(".prod_img img")['src']

                product_img = "https://" + product_img.split("//")[-1]

                tabs[product_name] = {'price': product_price, 'img': product_img, 'gift': gift}
            
            idx += 1

        datas[legend] = tabs

    return datas

if __name__ == "__main__":
    datas = POSTRequestAPI_Cu(os.environ.get("URL_CU"))

    for leg, products in datas.items():
        for product, data in products.items():
            print(product, data)