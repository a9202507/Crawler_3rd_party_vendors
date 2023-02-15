import requests
from bs4 import BeautifulSoup as bs
cs_url='https://eip.dediprog.com/dediprog/ic_search.php'
param= {'s_o_no':'',
        'ddlProgrammer[]':'80',
        'ddlProgrammer[]':'11',
#        'ddlProgrammer[]':'81',
#        'ddlProgrammer[]':'21',
#        'ddlProgrammer[]':'26',
        'ddlManuf':'767',       # ddlManuf=767 means Infineon
        "per_page_50":"100",
        }
r=requests.get(cs_url,params=param)
html=r.content.decode("utf-8")
print(r.url)
#print(html)

soup=bs(html,"html.parser")
#print(soup)

