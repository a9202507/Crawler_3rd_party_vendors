from flask import Flask, render_template, jsonify, abort, request
import os
import dediprog

app = Flask(__name__)
print(dir(app))
# print(app.config)
# 設定資源快取時間為零秒
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
author_name = "eason"
web_info = {
    "title": "歡迎來我的網站 Infineon 2023/02/15",
    "subtitle": "welcome HICP"
}

show_link = True
article_list = [
    {
        "id": "1",
        "title": "文章1",
        "subtitle": "副標題1",
        "content": "內文1",
    },
    {
        "id": "2",
        "title": "文章2",
        "subtitle": "副標題2",
        "content": "內文2",
    },
    {
        "id": "3",
        "title": "文章3",
        "subtitle": "副標題3",
        "content": "內文3",
    },
    {
        "id": "4",
        "title": "文章4",
        "subtitle": "副標題4",
        "content": "內文4",
    },
    {
        "id": "5",
        "title": "文章5",
        "subtitle": "副標題5",
        "content": "內文5",
    },

]


@app.route('/')
def hello():
    html = render_template("home.html",
                           web_info=web_info,
                           author_name=author_name,
                           show_link=show_link,
                           header_title="Infineon PL12 3rd party vendor query"
                           )
    return html


@app.route('/about')
def method_name():
    return render_template("about.html",
                           #header_title="about page",
                           )


@app.route('/article')
def article_list_page():
    return render_template("article-list.html",
                           header_title="py文章列表",
                           article_list=article_list,
                           )


@app.route('/dediprog')
def check_dediprog_status():
    html=dediprog.get_dediprog_html()
    return render_template("layout.html",content=html)

# 動態路由
@app.route('/article/<article_id>')  # <> 為flask的變數寫法
def article_page(article_id):
    article = None
    for a in article_list:
        if a['id'] == article_id:
            article = a
            break
    # 如果文章存在 就返回文章
    print(article)
    if article:
        return render_template("article/show.html",
                               article=article,
                               header_title=article['title'])
    else:
        # 如果文章不存在
        return render_template("article/not-found.html",
                               article_id=article_id,
                               header_title="查無文章")


tasks = [
    {
        'id': 1,
        'title': '電話費',
        'note': '500元',
        'done': False
    },
    {
        'id': 2,
        'title': '錄教學影片',
        'note': 'restAPI for todo',
        'done': False
    }
]


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/api/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [x for x in tasks if x['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task})


@app.route('/api/tasks', methods=['POST'])
def create_task():

    print(f"hello,{request.json}")
    if request.json is None or 'title' not in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id']+1,
        'title': request.json['title'],
        'note': request.json.get('note', ''),
        'done': False


    }

    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/api/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):

    print(f"id={task_id}")
    task = [x for x in tasks if x['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.route('/api/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    print(f"gg={request.json}")
    task = [x for x in tasks if x['id'] == task_id]
    if len(task) == 0:
        abort(404)

    if request.json is None:
        abort(400, "No JSON data!!!")
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400, "title field is not a string!!!")
    if 'note' in request.json and type(request.json['note']) != str:
        abort(400, "title field is not a string!!!")
    if 'done' in request.json and type(request.json['done']) != bool:
        abort(400, "title field is not a boolean!!!")

    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['note'] = request.json.get('note', task[0]['note'])
    task[0]['done'] = request.json.get('done', task[0]['done'])

    return jsonify({'task': task[0]})


def method_name():
    pass


if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)
    app.run(host='0.0.0.0', port=port)
    # test for OC 2022
