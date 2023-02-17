import requests
from bs4 import BeautifulSoup as bs


def get_dediprog_html(part_number):
    cs_url = 'https://eip.dediprog.com/dediprog/ic_search.php'
    param = {'s_o_no': part_number,
             'ddlProgrammer[]': '80',
             'ddlProgrammer[]': '11',
             #        'ddlProgrammer[]':'81',
             #        'ddlProgrammer[]':'21',
             #        'ddlProgrammer[]':'26',
             'ddlManuf': '767',       # ddlManuf=767 means Infineon
             "per_page_50": "100",
             }
    r = requests.get(cs_url, params=param)
    html = r.content.decode("utf-8")
    print(r.url)
    # print(html)

    soup = bs(html, "html.parser")
    # print(soup)
    return r


r = get_dediprog_html('xdpe1')
html = r.content.decode("utf-8")
soup = bs(html, "html.parser")
spans = soup.find_all('font', {'size': "-1"})

i = 0
for index, s in enumerate(spans):
    if index == 7+i*6:
        print(index, s.string)
        i += 1
print(f"number={i-1}")
