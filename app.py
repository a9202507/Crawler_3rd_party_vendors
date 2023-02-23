from flask import Flask, render_template, jsonify, abort, request
import os
import dediprog
import hilo

app = Flask(__name__)
print(dir(app))
# print(app.config)
# 設定資源快取時間為零秒
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def hello():
    html = render_template("home.html",
                           header_title="Search part number",
                           )
    return html


@app.route('/search_result', methods=['get'])
def check_all_vendors_status():
    part_number = request.values.get('part_number')
    if len(part_number) <= 2:
        return render_template("home.html", header_title="Need to enter 3 characters")

    else:
        # check hilo
        hilo_part_list = hilo.get_hilo_html(part_number)
        # check Dediprog
        dediprog_part_list = dediprog.get_dediprog_html(part_number)
        # check Acroview
        acroview_part_list = hilo.get_acroview_result(part_number)
        # check Elnec
        elnec_part_list = hilo.get_elnec_result(part_number)

        hilo_info = {'vendor_name': 'HiLo-System',
                     'website': 'https://www.hilosystems.com/en-gb/search',
                     'part_list': hilo_part_list,
                     'part_number': part_number,
                     }

        dediprog_info = {'vendor_name': 'DediProg',
                         'website': 'https://www.dediprog.com/search/socket?keyword=',
                         'part_list': dediprog_part_list,
                         'part_number': part_number,
                         }
        acroview_info = {'vendor_name': 'Acroview',
                         'website': 'https://www.acroview.cc/en-Chip-support-query/',
                         'part_list': acroview_part_list,
                         'part_number': part_number,
                         }
        elnec_info = {'vendor_name': 'Elnec',
                      'website': 'https://www.elnec.com/en/search/',
                      'part_list': elnec_part_list,
                      'part_number': part_number,
                      }

        search_result_list = list()

        search_result_list.append(dediprog_info)
        search_result_list.append(hilo_info)
        search_result_list.append(acroview_info)
        search_result_list.append(elnec_info)

        return render_template("search_result.html", search_result_list=search_result_list, header_title=f"Search keyword: '{part_number}' ")


if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)
    app.run(host='0.0.0.0', port=port, debug=True)
    # test for OC 2022
