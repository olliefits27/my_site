import requests

url = "http://127.0.0.1:8000/pokemon_api/3"

request = requests.get(url=url)
print(request)
print(request.text)