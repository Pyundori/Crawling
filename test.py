import requests

request_msg = "https://kauth.kakao.com/oauth/authorize?client_id=63dea6379cacab1fddbfce388d30a6bb&redirect_uri=http://54.180.109.216:5000/oauth2/callback&response_type=code"

params = {
    "client_id": "63dea6379cacab1fddbfce388d30a6bb",
    "redirect_uri": "http://54.180.109.216:5000/oauth2/callback",
    "response_type": "code",
}
res = requests.get("https://kauth.kakao.com/oauth/authorize", params=params)

with open("test.txt", "w") as f:
    f.write(res.text)