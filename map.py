import requests
import pprint

# 自分のAPIKEYを入力して下さい
API_KEY = ""

url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=ユニバーサル&components=country:jp&types=geocode&language=ja&types=geocode&key=" + API_KEY

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

res = response.json()

len_predictions = len(res["predictions"])

predictions = []
dict_description = {}