import src
import json
from flask import Flask

app = Flask(__name__)

PAGE_LIST = {
    'seven_eleven': 'https://www.7-eleven.co.kr/product/listMoreAjax.asp',
    'gs25': 'http://gs25.gsretail.com/gscvs/ko/products/event-goods-search',
    'emart24': 'https://www.emart24.co.kr/product/eventProduct.asp',
    'cu': 'https://cu.bgfretail.com/event/plusAjax.do',
}

@app.route("/")
def main():
    return "Hello!"

# main function
@app.route("/crawling")
def crawling():
    seven_eleven = src.POSTRequestAPI_SevenEleven(PAGE_LIST["seven_eleven"]) # 완료
    # with open("test_json/even_eleven.json", "w", encoding='utf-8') as f:
    #     f.write(json.dumps(seven_eleven, ensure_ascii=False))
    return seven_eleven

    gs25 = src.GETRequestAPI_Gs25(PAGE_LIST["gs25"]) # 완료
    # with open("test_json/gs25.json", "w", encoding='utf-8') as f:
    #     f.write(json.dumps(gs25, ensure_ascii=False))

    emart24 = src.GETRequestAPI_Emart24(PAGE_LIST['emart24']) # 완료
    # with open("test_json/emart24.json", "w", encoding='utf-8') as f:
    #     f.write(json.dumps(emart24, ensure_ascii=False))

    cu = src.POSTRequestAPI_Cu(PAGE_LIST['cu']) # 완료
    # with open("test_json/cu.json", "w", encoding='utf-8') as f:
    #     f.write(json.dumps(cu, ensure_ascii=False))

    
    None
 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)