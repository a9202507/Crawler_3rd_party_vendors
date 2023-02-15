import requests
from bs4 import BeautifulSoup

cs_url='https://www.tenlong.com.tw/tw/bestselling'
param= {'range':'30','page':'2'}
r=requests.get(cs_url,params=param)
html = r.content.decode("utf-8")

print(html)


