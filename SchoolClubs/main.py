from flask import Flask, render_template, url_for, request, redirect
from db.classes2 import *
import random
from datetime import datetime

app = Flask(__name__, static_folder="static")


def main():
    app.run()


@app.route('/')
@app.route('/index/')
def index():
    params = dict()
    params["clubs"] = []
    clubs = manager.get_items("club", "1")
    for club in clubs:
        params["clubs"].append({"id": club.get('id'), "name": club.get('name')})
    params["screen_image"] = "main-screen.jpg"
    params["screen_title"] = "КРУЖКИ ШКОЛЫ<br>2065"

    params["text_block"] = "Школьные кружки помогают детям узнавать что-то новое и интересное, знакомиться с новыми " \
                           "технологиями и увлекательными занятиями, раскрывать их таланты и находить свое призвание."

    params["clubs_search_form"] = False
    params["clubs_title"] = "На данный момент в нашей школе функционируют <b>25</b> кружков.<br>Вот самые популярные:"
    params["clubs_list"] = [
        {
            "id": 1,
            "name": "<h2>Математика</h2>"
        },
        {
            "id": 2,
            "name": "<h2>Робототехника</h2>"
        }
    ]

    params["teachers_rows"] = [
        [
            {
                "id": 1,
                "description": "Сталкер",
                "image": "teachers/melnik.jpg",
                "name": "Святослав",
                "surname": "Мельников",
                "middle_name": "Константинович",
            },
            {
                "id": 1,
                "description": "Сталкер",
                "image": "teachers/melnik.jpg",
                "name": "Святослав",
                "surname": "Мельников",
                "middle_name": "Константинович",
            },
            {
                "id": 1,
                "description": "Сталкер",
                "image": "teachers/melnik.jpg",
                "name": "Святослав",
                "surname": "Мельников",
                "middle_name": "Константинович",
            },
            {
                "id": 1,
                "description": "Сталкер",
                "image": "teachers/melnik.jpg",
                "name": "Святослав",
                "surname": "Мельников",
                "middle_name": "Константинович",
            }
        ]
    ]
    return render_template('index.html', params=params)


@app.route('/teachers/')
def teachers():
    params = dict()
    params["clubs"] = []
    clubs = manager.get_items("club", "1")
    for club in clubs:
        params["clubs"].append({"id": club.get('id'), "name": club.get('name')})
    params["teachers_row"] = [
        [
            {
                "id": 1,
                "description": "Учитель пинания бревна",
                "image": "teachers/1.jpg",
                "name": "Пинок",
                "surname": "Пинков",
                "middle_name": "Пинкович",
            }
        ]
    ]
    return render_template('index.html', params=params)


@app.route('/teacher/<teacher_id>/')
def teacher(teacher_id):
    params = dict()
    params["clubs"] = []
    params["clubs_search_form"] = False
    params["clubs_title"] = "Кирсанов Максим Григорьевич ведет <b>2</b> кружка:"
    params["clubs_list"] = [
        {
            "id": 1,
            "name": "<h2>Математика</h2>"
        },
        {
            "id": 2,
            "name": "<h2>Робототехника</h2>"
        }
    ]
    params["teacher_name"] = "Кирсанов Максим Григорьевич"
    params["teacher_description"] = "Учитель информатики и математики"
    params["teacher_image"] = "3.jpg"
    params["clubs_show_button"] = False
    return render_template('teacher.html', params=params)


@app.route('/club/<club_id>/')
def club(club_id):
    params = dict()
    params["screen_image"] = "clubs/1.jpg"
    params["screen_title"] = "Робототехника"

    params["text_block"] = "На этом кружке дети учатся конструировать и программировать роботов. Ребята приобретают " \
                           "навыки инженерного проектирования, программирования и разработки."
    params["teachers_title"] = "Кружок ведет:"
    params["all_teachers"] = True

    params["teachers_rows"] = [
        [
            {
                "id": 1,
                "description": "Сталкер",
                "image": "teachers/melnik.jpg",
                "name": "Святослав",
                "surname": "Мельников",
                "middle_name": "Константинович",
            }
        ]
    ]
    params["club"] = 1
    clubs = manager.get_items("club", "1")
    params["clubs"] = []
    for club in clubs:
        params["clubs"].append({"id": club.get('id'), "name": club.get('name')})
    return render_template('club.html', params=params)


@app.route('/statement_handler/', methods=['POST', 'GET'])
def statement_handler():
    if request.method == 'POST':
        args = dict()
        for key in request.form:
            args[key] = request.form[key]
        args['track_code'] = random.choice(['a', 'b', 'c', 'd', 'e']) + \
                             random.choice(['a', 'b', 'c', 'd', 'e']) + \
                             random.choice(['a', 'b', 'c', 'd', 'e']) + str(random.randint(1000, 10000))
        args['statement_ip'] = request.remote_addr
        args['statement_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_statement = Statement(manager, **args)
        users_statements = manager.get_items('statement', f"`statement_ip` = '{request.remote_addr}'")
        if users_statements is None:
            new_statement.add_to_db()
            db.commit()
        else:
            if len(users_statements) < 10:
                new_statement.add_to_db()
        return redirect("http://yandex.ru/maps", code=302)
    return ''


if __name__ == '__main__':
    main()