from flask import Flask, render_template, url_for, request, redirect
from db.classes2 import *
import random
from datetime import datetime
from statement import createStatement

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
    tc = User(manager, id=teacher_id, type_id=3).fields
    gr = manager.get_items('club_group', 'teacher_id=' + teacher_id)
    cl = []
    if gr:
        for group in gr:
            c = Club(manager, id=group.fields["club_id"]).fields
            if c not in cl:
                cl.append(c)

    information = [{"id": club["id"], "name": "<h2>" + club["name"] + "</h2>"} for club in cl]
    name = tc['surname'] + ' ' + tc['name'] + ' ' + tc['middle_name']

    if gr:
        num_of_clubs = len(cl)
        if 5 <= num_of_clubs <= 20:
            num_of_clubs = " ведет <b>" + str(num_of_clubs) + "</b> кружков:"
        elif 2 <= num_of_clubs % 10 <= 4:
            num_of_clubs = " ведет <b>" + str(num_of_clubs) + "</b> кружка:"
        elif num_of_clubs % 10 == 1:
            num_of_clubs = " ведет <b>" + str(num_of_clubs) + "</b> кружок:"
        else:
            num_of_clubs = " ведет <b>" + str(num_of_clubs) + "</b> кружков:"
    else:
        num_of_clubs = " не ведет кружков."

    params = dict()
    params["clubs"] = cl
    if len(cl) > 10:
        params["clubs_search_form"] = True
    else:
        params["clubs_search_form"] = False
    params["clubs_title"] = name + num_of_clubs
    params["clubs_list"] = information
    params["teacher_name"] = name
    params["teacher_description"] = tc["description"]
    params["teacher_image"] = tc["image"]
    params["clubs_show_button"] = False
    return render_template('teacher.html', params=params)


@app.route('/club/<club_id>/')
def club(club_id):
    cl = Club(manager, id=club_id).fields
    gr = manager.get_items('club_group', 'club_id=' + club_id)
    tc = []
    groups = []
    if gr:
        for group in gr:
            t = User(manager, id=group.fields["club_id"]).fields
            if t not in tc:
                tc.append(t)

            groups.append({
                "name": group.fields["name"],
                "teacher_name": t["surname"] + ' ' + t["name"] + ' ' + t["middle_name"],
                "lessons": [
                    {
                        "start": lesson.fields["start"],
                        "finish": lesson.fields["finish"],
                        "day": lesson.fields["day"],
                        "cabinet": lesson.fields["cabinet"]
                    }
                    for lesson in manager.get_items('club_group_lesson', 'group_id=' + str(group.fields["id"]))
                ]
            })

    main_teacher = [[{
        "id": teacher['id'],
        "description": teacher["description"],
        "image": teacher["image"],
        "name": teacher["name"],
        "surname": teacher["surname"],
        "middle_name": teacher["middle_name"],
    }
        for teacher in tc]]

    params = dict()
    params['menu_current_page'] = 'clubs'
    params["screen_image"] = cl['image']
    params["screen_title"] = cl['name']

    params["text_block"] = cl['description']
    params["teachers_title"] = "Кружок ведет:"
    params["all_teachers"] = True

    params["teachers_rows"] = main_teacher
    params["club_groups"] = groups
    params["club"] = 1
    
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
        createStatement(manager, str(Statement(manager, 'track_code=' + args['track_code']).fields['id']))
        return redirect("http://yandex.ru/maps", code=302)
    return ''


if __name__ == '__main__':
    main()
