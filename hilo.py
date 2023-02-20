import urllib.request as req
from urllib import parse
import json


def get_hilo_html(part_number):
    url = 'https://www.hilosystems.com/search/ajaxLoadData'
    data = parse.urlencode({"ic_name": part_number}).encode()
    request = req.Request(url,
                          data=data,
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
                                   })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    json_data = json.loads(data)

    result_list = list()

    for i in range(0, len(json_data['data']['data_array'])):
        result_list.append(json_data['data']['data_array'][i]['I_IC'])

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
        for i in range(0, len(json_data['data'])):
            result_list.append(json_data['data'][i]['chip'])
    except:
        result_list.append("No match")

    return result_list


if __name__ == "__main__":

    data = get_acroview_result('xdpe1')
