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
             #'ddlManuf':'767',       # ddlManuf=767 means Infineon
             "per_page_50": "100",
             }
    r = requests.get(cs_url, params=param)
    html = r.content.decode("utf-8")
    print(r.url)
    # print(html)

    soup = bs(html, "html.parser")
    # print(soup)




    soup = bs(html, "html.parser")
    spans = soup.find_all('font', {'size': "-1"})

    i = 0
    result_part_number_list=list()
    for index, s in enumerate(spans):
        if index == 7+i*6:
            result_part_number_list.append(s.string)
            i += 1

    new_list=result_part_number_list[0:-1]

    final_result_part_number_list=list()
    for s in new_list:
        if s  != None:
            final_result_part_number_list.append(s[2:])

    return final_result_part_number_list


if __name__ == "__main__":

    part_list=get_dediprog_html('xdpe192c')

    print(part_list)
