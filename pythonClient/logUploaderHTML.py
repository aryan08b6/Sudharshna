import requests
from logCollector import getLog

url = "localhost:5000/applogs"
for x in getLog("Application", 20):
    res = requests.post(url, json=x)
    print(res)

