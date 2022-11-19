import requests
import pprint
import settings

# 自分のAPIKEYを入力して下さい

url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=ユニバーサル&components=country:jp&types=geocode&language=ja&types=geocode&key=" + settings.AP

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

res = response.json()

len_predictions = len(res["predictions"])

predictions = []
dict_description = {}