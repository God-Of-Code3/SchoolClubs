from docxtpl import DocxTemplate
from SchoolClubs.db.classes2 import Statement, Club
from pathlib import Path


STTMNT_TMPLT = Path("./static/doc/statement template.docx")
MONTHS = ['января', 'февраля', 'марта', 'апреля',
          'мая', 'июня', 'июля', 'августа',
          'сентября', 'октября', 'ноября', 'декабря']


def createStatement(manager, st_id):
    try:
        if st_id.isdigit():
            st = Statement(manager, id=str(st_id)).fields
        else:
            st = Statement(manager, track_code=str(st_id)).fields
        club = Club(manager, id=str(st['club_id'])).get('name')

        doc = DocxTemplate(STTMNT_TMPLT.resolve())
    except Exception as e:
        print('Error:', e)
    else:
        print(st)

        context = {}
        context['club'] = club

        for val in list(st.keys()):
            if val == 'child_gender':
                if st[val] == 1:
                    context[val] = 'мужской'
                else:
                    context[val] = 'женский'
            elif val == 'document_type':
                if st[val] == 1:
                    context[val] = 'паспорт'
                else:
                    context[val] = 'свидетельство о рождении'
            else:
                context[val] = st[val]

        context['day'] = st['statement_datetime'].day
        context['month'] = MONTHS[int(st['statement_datetime'].month) - 1]
        context['year'] = int(st['statement_datetime'].year) % 2000

        doc.render(context)
        doc.save(club + ' ' + str(st['child_surname']) + ".docx")
