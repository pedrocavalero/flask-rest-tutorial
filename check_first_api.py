import requests
url = "http://127.0.0.1:5000/1"
response = requests.get(url=url)
print(response.text)