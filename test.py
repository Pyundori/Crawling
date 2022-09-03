import requests


response = requests.post('https://www.7-eleven.co.kr/product/listMoreAjax.asp', data={
    "intPageSize": 10, 
    "intCurrPage":0, 
    "cateCd1":"", 
    "cateCd2":"", 
    "cateCd3":"", 
    "pTab":1
}).text


print(response)