import urllib.request as req
from urllib import parse
import json

import requests  # for get method
from bs4 import BeautifulSoup as bs


def search_with_hilo(part_number):
    url = 'https://www.hilosystems.com/search/ajaxLoadData'
    # table_name=3 mean Hilo All-200
    data = parse.urlencode({"ic_name": part_number, "table_name": 3}).encode()
    request = req.Request(url,
                          data=data,
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
                                   })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    json_data = json.loads(data)

    result_list = list()

    # for i in range(0, len(json_data['data']['data_array'])):
    for index, data in enumerate(json_data['data']['data_array']):
        result_list.append(json_data['data']['data_array'][index]['I_IC'])

    if len(result_list) == 0:
        result_list.append("No match")

    return result_list


def search_with_acroview(part_number):
    url = 'https://www.acroview.com/support/_list/num/20/page/1'
    data = parse.urlencode({"chip": part_number}).encode()
    request = req.Request(url,
                          data=data,
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
                                   })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    json_data = json.loads(data)
    result_list = list()
    try:
        # for index in range(0, len(json_data['data'])):
        for index, data in enumerate(json_data['data']):
            result_list.append(json_data['data'][index]['chip'])
    except:
        result_list.append("No match")

    return result_list


def search_with_elnec(part_number):
    url = 'https://www.elnec.com/ajax-devices.php'
    data = parse.urlencode({"json": part_number}).encode()
    request = req.Request(url,
                          data=data,
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
                                   })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    soup = bs(data, "html.parser")
    temp_list = soup.find_all("li")

    result_list = list()

    for item in temp_list:
        result_list.append(item.get_text(strip=True))

    if not result_list:
        result_list.append("No match")

    return result_list


def search_with_dediprog(part_number):
    cs_url = 'https://eip.dediprog.com/dediprog/ic_search.php'
    param = {'s_o_no': part_number,
             'ddlProgrammer[]': '80',
             'ddlProgrammer[]': '11',
             #        'ddlProgrammer[]':'81',
             #        'ddlProgrammer[]':'21',
             #        'ddlProgrammer[]':'26',
             # 'ddlManuf':'767',       # ddlManuf=767 means Infineon
             "per_page_50": "100",
             }
    r = requests.get(cs_url, params=param)
    html = r.content.decode("utf-8")

    # print(html)

    soup = bs(html, "html.parser")
    # print(soup)

    soup = bs(html, "html.parser")
    spans = soup.find_all('font', {'size': "-1"})

    i = 0
    result_part_number_list = list()
    for index, s in enumerate(spans):
        if index == 7+i*6:
            result_part_number_list.append(s.string)
            i += 1

    new_list = result_part_number_list[0:-1]

    final_result_part_number_list = list()
    for s in new_list:
        if s != None:
            final_result_part_number_list.append(s[2:])

    if len(final_result_part_number_list) == 0:
        final_result_part_number_list.append("No match")

    return final_result_part_number_list, str(r.url)
