import requests
from bs4 import BeautifulSoup as bs

import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

def POSTRequestAPI_SevenEleven(url):
    # legends = ['1N1', '2N1', 'GIFT', 'SALE']
    # 1+1 : fncMore(1)
    # 2+1 : fncMore(2)
    # 증정 : fncMore(2)
    # 할인 : fncMore(4)

    datas = {}
    for pTab, legend in enumerate(['1N1', '2N1', 'GIFT', 'SALE']):
        i = 0
        tabs = {}
        while True:
            response = requests.post(url, data={
                "intPageSize": 10, 
                "intCurrPage":i, 
                "cateCd1":"", 
                "cateCd2":"", 
                "cateCd3":"", 
                "pTab":pTab+1
            }).text
            soup = bs(response, 'html.parser')

            if soup.find("div", attrs={"class": "pic_product"}) is None:
                break

            for li_item in soup.select("li"):
                gift = None
                try:
                    product_data = li_item.select(".pic_product")[0]
                    product_name = product_data.select(".name")[0].text
                    product_price = product_data.select(".price")[0].select("span")[0].text.replace(",", "")
                    product_price = int(product_price)
                    product_img = "https://www.7-eleven.co.kr" + product_data.select(".pic_product")[0].find("img")['src']

                    tabs[product_name] = {'price': product_price, 'img': product_img, 'gift': gift}
                    
                except:
                    None
            i += 1

        datas[legend] = tabs
    return datas