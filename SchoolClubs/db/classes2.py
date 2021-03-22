from db.methods import *


class DB:
    def __init__(self):
        self.connection = create_connection("141.8.194.42", "a0286951_school_clubs_admin", "Ev19ABr8cc6",
                                            "a0286951_school-clubs")
        self.cursor = self.connection.cursor()
        self.queries = []

    def query(self, query):
        try:
            self.cursor.execute(query)
            self.queries.append(query)
            result = self.cursor.fetchall()

            return result
        except Error as e:
            return "-1"

    def commit(self):
        self.connection.commit()


db = DB()


class Manager:
    def __init__(self, db):
        self.db = db

    def get_data(self, table_name, **kwargs):
        query = f"SELECT * FROM `{table_name}` WHERE "
        for i, key in enumerate(kwargs.keys()):
            if i != 0:
                query += "AND "
            query += f"`{key}` = '{kwargs[key]}'"
        result = self.db.query(query)

        if len(result) > 0:
            keys = self.db.cursor.column_names
            values = dict()
            for i, key in enumerate(keys):
                values[key] = result[0][i]
            return values

    def get_items(self, table, condition):
        query = f"SELECT * FROM `{table}` WHERE " + condition
        result = self.db.query(query)
        if len(result) > 0:
            keys = self.db.cursor.column_names
            items = []
            for row in result:
                fields = dict()
                for i, key in enumerate(keys):
                    fields[key] = row[i]
                items.append(CLASSES[table](self, add=False, select=False, **fields))
            return items

    def add_item(self, table_name, identificator, **kwargs):
        query = f"INSERT INTO `{table_name}` ("
        for i, key in enumerate(kwargs.keys()):
            if key != identificator:
                query += f"`{key}`"
                if i < len(kwargs.keys()) - 1:
                    query += ", "
        query += ") VALUES ("
        for i, key in enumerate(kwargs.keys()):
            if key != identificator:
                query += f"'{kwargs[key]}'"
                if i < len(kwargs.keys()) - 1:
                    query += ", "
        query += ")"
        self.db.query(query)
        query = f"SELECT `{identificator}` FROM `{table_name}` WHERE 1 ORDER BY `{identificator}` DESC LIMIT 1"
        result = self.db.query(query)
        return result[0][0]

    def remove_item_query(self, table, identificator):
        query = [table, f"DELETE FROM `{table}` WHERE "]
        query[1] += identificator

        if RELATIONS[table]["down"] is not None:
            for rel in RELATIONS[table]["down"]:
                query2 = f"SELECT `{RELATIONS[table]['down'][rel][0]}` FROM `{table}` WHERE "
                query2 += identificator
                query.extend(self.remove_item_query(rel, f"`{RELATIONS[table]['down'][rel][1]}` IN " + "(" +
                                                    query2 + ")"))
        return query

    def remove_item(self, table, item_identificator, item_identificator_value):
        identificator = f"`{item_identificator}` = '{item_identificator_value}'"
        queries = list(reversed([q for q in self.remove_item_query(table, identificator) if "DELETE" in q]))

        for q in queries:
            self.db.query(q)

    def remove_items(self, table, condition):
        items = self.get_items(table, condition)
        if items is not None:
            for item in items:
                item.remove_from_db()

    def update_item(self, table, identificator, fields):
        query = f"UPDATE `{table}` SET "
        for i, key in enumerate(fields.keys()):
            if key != identificator:
                query += f"`{key}` = '{fields[key]}'"
            if i < len(fields.keys()) - 1:
                query += ", "
        query += f" WHERE `{identificator}` = '{fields[identificator]}'"
        self.db.query(query)

    def update_items(self, table, condition, fields):
        items = self.get_items(table, condition)
        if items is not None:
            for item in items:
                for key in fields:
                    item.set(key, fields[key])
                item.update()

    def authorize_user(self, login, password):
        condition = f"`login` = '{login}' AND `password` = '{hash_password(password)}' LIMIT 1"
        items = self.get_items("user", condition)
        if len(items) > 0:
            return items[0]
        return False


manager = Manager(db)


class TableItem:
    def __init__(self, manager, table_name="", identificator_field="id", add=False, select=True,
                 **kwargs):
        self.manager = manager
        self.table_name = table_name
        self.identificator_field = identificator_field
        self.fields = dict()
        for key in kwargs:
            self.fields[key] = kwargs[key]
        if self.fields[self.identificator_field] is not None and select:
            identificators = {
                self.identificator_field: self.fields[self.identificator_field]
            }
            values = self.manager.get_data(table_name, **identificators)
            if values is not None:
                self.fields = values
        if add:
            self.add_to_db()

    def add_to_db(self):
        if self.fields[self.identificator_field] is None:
            identificator = self.manager.add_item(self.table_name, self.identificator_field, **self.fields)
            self.fields[self.identificator_field] = identificator

    def remove_from_db(self):
        self.manager.remove_item(self.table_name, self.identificator_field, self.fields[self.identificator_field])

    def update(self):
        self.manager.update_item(self.table_name, self.identificator_field, self.fields)

    def get(self, key):
        if key in self.fields:
            return self.fields[key]

    def set(self, key, value):
        if key in self.fields:
            self.fields[key] = value
            return True
        return False

    def __str__(self):
        string = "\n---=== " + self.table_name + " ===---\n"
        for field in self.fields:
            string += f"{field}: '{self.fields[field]}'\n"
        relations_up = RELATIONS[self.table_name]["up"]
        relations_down = RELATIONS[self.table_name]["down"]
        if relations_down is not None:
            string += "\n\n--- Relations down ---\n"
            for relation in relations_down:
                string += f"table: '{relation}'; self field: '{relations_down[relation][0]}'; other's field: '" \
                          f"{relations_down[relation][1]}'\n"
        if relations_up is not None:
            string += "\n\n--- Relations up ---\n"
            for relation in relations_up:
                string += f"table: '{relation}'; self field: '{relations_up[relation][0]}'; other's field: '" \
                          f"{relations_up[relation][1]}'\n"
        return string

    def __repr__(self):
        return self.__str__()

    def __call__(self, key):
        if key in self.fields:
            return self.fields[key]


RELATIONS = {
    "statement": {
        "up": None,
        "down": None
    },
    "user": {
        "up": {"user_type": ["type_id", "id"]},
        "down": None
    },
    "club": {
        "up": {"user_type": ["type_id", "id"]},
        "down": {"club_group": ["id", "club_id"]}
    },
    "club_group": {
        "up": {"club": ["club_id", "id"], "user": ["teacher_id", "id"]},
        "down": {"club_group_lesson": ["id", "group_id"]}
    },
    "club_group_lesson": {
        "up": {"club_group": ["group_id", "id"], "user": ["teacher_id", "id"]},
        "down": None
    },
    "club_category": {
        "up": None,
        "down": {"club": ["id", "category_id"]}
    },
    "user_type": {
        "up": None,
        "down": {"user": ["id", "type_id"]}
    },
}


class User(TableItem):
    def __init__(self, manager, add=False, select=True, id=None, type_id=1, name="Иван", surname="Иванов",
                 middle_name="Иванович",
                 description="Пользователь", login="login1", password="password", image="user1.png"):
        args = {
            "id": id,
            "type_id": type_id,
            "name": name,
            "surname": surname,
            "middle_name": middle_name,
            "description": description,
            "login": login,
            "password": hash_password(password),
            "image": image
        }
        if id is not None:
            args["password"] = password
        super().__init__(manager, "user", "id", add=add, select=select, **args)


class Statement(TableItem):
    def __init__(self, manager, add=False, select=True, id=None, parent_name="", parent_surname="",
                 parent_middle_name="", parent_phone="", child_name="", child_surname="", child_middle_name="",
                 child_gender=1, child_birthday="2006-01-17", document_type=0, document_series="",
                 document_number="", document_date="2006-01-24", track_code="", club_id=0,
                 statement_datetime="2021-03-22:23:39:00", statement_ip="127.0.0.1"):
        args = {
            "id": id,
            "parent_name": parent_name,
            "parent_surname": parent_surname,
            "parent_middle_name": parent_middle_name,
            "parent_phone": parent_phone,
            "child_name": child_name,
            "child_surname": child_surname,
            "child_middle_name": child_middle_name,
            "child_gender": child_gender,
            "child_birthday": child_birthday,
            "document_type": document_type,
            "document_series": document_series,
            "document_number": document_number,
            "document_date": document_date,
            "statement_datetime": statement_datetime,
            "statement_ip": statement_ip
        }
        super().__init__(manager, "statement", "id", add=add, select=select, **args)


class Club(TableItem):
    def __init__(self, manager, add=False, select=True, id=None, category_id=1, name="Безымянный кружок",
                 description="Описание безымянного кружка", max_student=10, price=0, gender=-1, age=""):
        args = {
            "id": id,
            "category_id": category_id,
            "name": name,
            "description": description,
            "max_student": max_student,
            "price": price,
            "gender": gender,
            "age": age
        }
        super().__init__(manager, "club", "id", add=add, select=select, **args)


class Group(TableItem):
    def __init__(self, manager, add=False, select=True, id=None, name="Безымянная группа", club_id=1, teacher_id=0):
        args = {
            "id": id,
            "name": name,
            "club_id": club_id,
            "teacher_id": teacher_id
        }
        super().__init__(manager, "club_group", "id", add=add, select=select, **args)


class Lesson(TableItem):
    def __init__(self, manager, add=False, select=True, id=None, start="14:00:00", finish="16:00:00", day=1,
                 group_id=0, cabinet="3-B1"):
        args = {
            "id": id,
            "start": start,
            "finish": finish,
            "day": day,
            "group_id": group_id,
            "cabinet": cabinet
        }
        super().__init__(manager, "club_group_lesson", "id", add=add, select=select, **args)


class UserType(TableItem):
    def __init__(self, manager, add=False, select=True, id=None, name="Новый тип пользователя"):
        args = {
            "id": id,
            "name": name
        }
        super().__init__(manager, "user_type", "id", add=add, select=select, **args)


class ClubCategory(TableItem):
    def __init__(self, manager, add=False, select=True, id=None, name="Новая категория кружка"):
        args = {
            "id": id,
            "name": name
        }
        super().__init__(manager, "club_category", "id", add=add, select=select, **args)


CLASSES = {
    "user": User,
    "club_group": Group,
    "club_group_lesson": Lesson,
    "statement": Statement,
    "club_category": ClubCategory,
    "user_type": UserType
}

"""
Объявление объекта
1) с нуля
club = Club(manager, name='Рисование', description='Рисовательный кружок имени Шишкина.', ... )
2) по id
club = Club(manager, id=1)

Добавление объектов в базу
club.add_to_db()

Изменение свойств объекта
club.set('name', 'Изобразительное искусство')

Сохранение изменений в базу
club.update()

Удаление объекта из базы
club.remove_from_db()

ИЗМЕНЕНИЯ НУЖНО СОХРАНЯТЬ В БАЗЕ НА СЕРВЕРЕ, ПОЭТОМУ
db.commit()

"""