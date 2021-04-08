from flask import Flask, render_template, url_for, request, redirect
from db.classes2 import *
import random
from datetime import datetime
from statement import createStatement

app = Flask(__name__, static_folder="static", )


def main():
    app.run()


@app.route('/')
@app.route('/index/')
def index():
    params = dict()
    params['menu_current_page'] = 'main'
    params["clubs"] = []
    clubs = manager.get_items("club", "1")
    for club in clubs:
        params["clubs"].append({"id": club.get('id'), "name": "<h2>" + club.get('name') + "</h2>"})
    params["screen_image"] = "main-screen.jpg"
    params["screen_title"] = "КРУЖКИ ШКОЛЫ<br>2065"

    params["text_block"] = "Школьные кружки помогают детям узнавать что-то новое и интересное, знакомиться с новыми " \
                           "технологиями и увлекательными занятиями, раскрывать их таланты и находить свое призвание."

    params["clubs_search_form"] = False

    printed_clubs = 5
    if clubs:
        num_of_clubs = len(clubs)
        if 5 <= num_of_clubs <= 20:
            num_of_clubs = str(num_of_clubs) + "</b> кружков"
        elif 2 <= num_of_clubs % 10 <= 4:
            num_of_clubs = str(num_of_clubs) + "</b> кружка"
        elif num_of_clubs % 10 == 1:
            num_of_clubs = str(num_of_clubs) + "</b> кружок"
        else:
            num_of_clubs = str(num_of_clubs) + "</b> кружков"

        if len(clubs) > printed_clubs:
            num_of_clubs = "функционируют <b>" + num_of_clubs + ".<br>Вот самые популярные:"
        else:
            num_of_clubs = "функционируют <b>" + num_of_clubs + ":"
    else:
        num_of_clubs = "нет ни одного кружка."

    params["clubs_title"] = "На данный момент в нашей школе " + num_of_clubs

    params["clubs_list"] = []
    lessons = []
    for club in params["clubs"]:
        lessons.append({"club": club, "lessons": 0})
        gr = manager.get_items('club_group', 'club_id=' + str(club.get("id")))
        if gr:
            for group in gr:
                lessons[-1]["lessons"] += len(
                    manager.get_items('club_group_lesson', 'group_id=' + str(group.get("id"))))

    for _ in range(len(clubs)):
        max_lessons = max([club["lessons"] for club in lessons])
        for club in lessons:
            if club["lessons"] == max_lessons:
                params["clubs_list"].append(club["club"])
                for c in range(len(lessons)):
                    if lessons[c] == club:
                        del lessons[c]
                        break
    if len(clubs) > printed_clubs:
        params["clubs_list"] = params["clubs_list"][:printed_clubs]

    params["teachers_rows"] = []
    teachers = manager.get_items("user", "`type_id` = '3' LIMIT 8")
    for i, teacher in enumerate(teachers):
        if i % 4 == 0:
            params["teachers_rows"].append([])
        params["teachers_rows"][-1].append({
            "href": '..' + url_for('teacher', teacher_id=str(teacher.get('id'))),
            "description": teacher.get('description'),
            "image": teacher.get('image'),
            "name": teacher.get('name'),
            "surname": teacher.get('surname'),
            "middle_name": teacher.get('middle_name')
        })
    return render_template('index.html', params=params)


@app.route('/teachers/')
def teachers():
    params = dict()
    params['menu_current_page'] = 'teachers'
    params["teachers_rows"] = []
    teachers = manager.get_items("user", "`type_id` = '3'")
    for i, teacher in enumerate(teachers):
        if i % 4 == 0:
            params["teachers_rows"].append([])
        params["teachers_rows"][-1].append({
            "href": '..' + url_for('teacher', teacher_id=str(teacher.get('id'))),
            "description": teacher.get('description'),
            "image": teacher.get('image'),
            "name": teacher.get('name'),
            "surname": teacher.get('surname'),
            "middle_name": teacher.get('middle_name')
        })
    params["all_teachers"] = True
    return render_template('all_teachers.html', params=params)


@app.route('/teacher/<teacher_id>/')
def teacher(teacher_id):
    tc = User(manager, id=teacher_id).fields
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
    params['menu_current_page'] = 'teachers'
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


@app.route('/clubs/')
def clubs():
    params = dict()
    params['menu_current_page'] = 'clubs'

    params["clubs_list"] = []
    clubs = manager.get_items("club", "1")
    for club in clubs:
        params["clubs_list"].append({"id": club.get('id'), "name": "<h2>" + club.get('name') + "</h2>"})

    if len(clubs) > 5:
        params["clubs_search_form"] = True
    #params["clubs_search_form"] = True
    params["clubs_title"] = "Список наших кружков (<b>" + str(len(clubs)) + "</b>):"
    params["clubs_categories"] = [{"id": category.get('id'), "name": category.get('name')}
                                  for category in manager.get_items("club_category", "True")]

    return render_template('all_clubs.html', params=params)


@app.route('/club/<club_id>/')
def club(club_id):
    params = dict()
    params['menu_current_page'] = 'clubs'
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
    params["club_groups"] = [
        {
            "name": "Дошкольники",
            "teacher_name": "Кирсанов Максим Григорьевич",
            "lessons": [
                {
                    "start": "14:00",
                    "finish": "16:00",
                    "day": "Понедельник",
                    "cabinet": "B45"
                },
                {
                    "start": "14:00",
                    "finish": "16:00",
                    "day": "Вторник",
                    "cabinet": "B45"
                },
                {
                    "start": "14:00",
                    "finish": "16:00",
                    "day": "Пятница",
                    "cabinet": "B45"
                }
            ]
        },
        {
            "name": "Шкульники",
            "teacher_name": "Мельников Святослав Константинович",
            "lessons": [
                {
                    "start": "14:00",
                    "finish": "16:00",
                    "day": "Понедельник",
                    "cabinet": "B35"
                },
                {
                    "start": "14:00",
                    "finish": "16:00",
                    "day": "Вторник",
                    "cabinet": "B35"
                },
                {
                    "start": "14:00",
                    "finish": "16:00",
                    "day": "Пятница",
                    "cabinet": "B35"
                }
            ]
        }
    ]
    params["club"] = 1
    clubs = manager.get_items("club", "1")
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
        createStatement(manager, str(new_statement.fields['id']))
        return redirect("http://yandex.ru/maps", code=302)
    return ''

@app.route('/search_form/', methods=['POST', 'GET'])
def search_form():
    if request.method == 'POST':
        args = dict()
        for key in request.form:
            args[key] = request.form[key]

        if args['club_id'] == '0':
            result = manager.get_items('club', 'True')
        else:
            result = manager.get_items('club', 'category_id=' + args['club_id'])

        print(args['club_id'])

        if args['search']:
            result = [club for club in result
                      if args['search'].lower() in club.get('name').lower() or\
                      args['search'].lower() in club.get('description').lower()]

        if args['sort_by'] == '0':
            sorted_result = result
        elif args['sort_by'] == '1':
            sorted_result = []
            for_sorting = {}
            for club in result:
                for_sorting[club.get('name')] = club
            keys = list(for_sorting.keys())
            keys.sort()
            for key in keys:
                sorted_result.append(for_sorting[key])
        elif args['sort_by'] == '2':
            sorted_result = []
            for_sorting = {}
            for club in result:
                for_sorting[club.get('age')] = club
            keys = list(for_sorting.keys())
            keys.sort()
            for key in keys:
                sorted_result.append(for_sorting[key])

        params = dict()
        params['menu_current_page'] = 'clubs'

        params["clubs_list"] = []
        clubs = sorted_result
        for club in clubs:
            params["clubs_list"].append({"id": club.get('id'), "name": "<h2>" + club.get('name') + "</h2>"})

        params["clubs_search_form"] = False

        if sorted_result:
            params["clubs_title"] = "Результаты поиска (<b>" + str(len(clubs)) + "</b>):"
        else:
            params["clubs_title"] = "По этому запросу ничего не найдено"
        params["clubs_categories"] = [{"id": category.get('id'), "name": category.get('name')}
                                      for category in manager.get_items("club_category", "True")]

        return render_template('all_clubs.html', params=params)
    return ''


if __name__ == '__main__':
    main()
