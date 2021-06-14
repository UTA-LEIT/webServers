import requests

for i in range(100):
    r = requests.get('http://localhost:8020/')
    print (i)