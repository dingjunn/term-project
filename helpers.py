import requests
import pprint

ticker = 'tsla' 
parameter = 'price'

url = f"https://yahoo-finance127.p.rapidapi.com/{parameter}/{ticker}"

headers = {
	"X-RapidAPI-Key": "c72f7a4367mshfe65ee4a74a894fp176ec0jsn93a89c3102d3",
	"X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

pprint.pprint(response.text)
