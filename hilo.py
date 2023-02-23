import urllib.request as req
from urllib import parse
import json
from bs4 import BeautifulSoup as bs


def get_hilo_html(part_number):
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


def get_acroview_result(part_number):
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


def get_elnec_result(part_number):
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

    if not result_list :
        result_list.append("No match")

    '''
    result_list = list()
    try:
        #for index in range(0, len(json_data['data'])):
        for index,data in enumerate(json_data['data']):
            result_list.append(json_data['data'][index]['chip'])
    except:
        result_list.append("No match")
    '''
    return result_list


if __name__ == "__main__":

    result_list = get_elnec_result('xdpe1192')
    print(result_list)
