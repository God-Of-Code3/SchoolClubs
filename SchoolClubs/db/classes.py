from db.methods import *


class DB:
    def __init__(self):
        self.connection = create_connection("141.8.194.42", "a0286951_school-clubs", "umfx1113442006RIMERNICK",
                                        "a0286951_school-clubs")
        self.cursor = self.connection.cursor()
        print(self.cursor)

    def query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            return result
        except Error as e:
            return "-1"

    def commit(self):
        self.connection.commit()


class TableItem:
    def __init__(self, manager, id):
        self.manager = manager
        self.id = id
        self.in_db = False

    def insert(self, id):

        self.id = id
        self.in_db = True


class User(TableItem):
    def __init__(self, manager, type_id=1, name="Иван", surname="Иванов", middle_name="Иванович", description="",
                 login="login1",
                 password="password", id=None):
        super().__init__(manager, id)
        self.type_id = type_id
        self.name = name
        self.surname = surname
        self.middle_name = middle_name
        self.description = description
        self.login = login
        self.password = hash_password(password)
        self.image = ""
        if id is not None:
            data = self.manager.get_user_data_by_id(id)
            print(data[0])
            if len(data) > 0:
                self.type_id = data[0][1]
                self.name = data[0][2]
                self.surname = data[0][3]
                self.middle_name = data[0][4]
                self.login = data[0][5]
                self.password = data[0][6]
                self.description = data[0][7]
                self.image = data[0][8]
                self.in_db = True

    def __str__(self):
        return f"Пользователь {self.surname} {self.name} {self.middle_name}, {self.description}, " \
               f"Логин: '{self.login}', Пароль (хешированный): '{self.password}' с id {self.id}"

    def __repr__(self):
        return self.__str__()


class GroupMember(TableItem):
    def __init__(self, manager, member_id=None, group_id=None, member=None, group=None, id=None):
        super().__init__(manager, id)
        self.group = group
        self.member = member
        self.member_id = member_id
        self.group_id = group_id

        if id is not None:
            data = self.manager.get_group_member_data_by_id(id)
            print(data[0])
            if len(data) > 0:
                self.member_id = data[0][2]
                self.group_id = data[0][1]
                self.in_db = True

        if self.group is not None:
            if self.group.in_db:
                if not self.in_db:
                    self.group_id = self.group.id
            else:
                self.group_id = None

        if self.member is not None:
            if self.member.in_db:
                if not self.in_db:
                    self.member_id = self.member.id
            else:
                self.member_id = None

    def link(self, group=None, member=None, group_id=None, member_id=None):
        if group is not None:
            self.group = group
            if group.in_db:
                self.group_id = group.id

        else:
            self.group_id = group_id

        if member is not None:
            self.member = member
            if member.in_db:
                self.member_id = member.id

        else:
            self.member_id = member_id

    def __str__(self):
        return f"Связка ученик-группа (ученик с id {self.member_id}) (группа с id {self.group_id}) с id {self.id}"

    def __repr__(self):
        return self.__str__()


class Member(TableItem):
    def __init__(self, manager, name="Иван", surname="Иванов", middle_name="Иванович",
                 age=15, cls="9a", id=None):
        super().__init__(manager, id)
        self.name = name
        self.surname = surname
        self.middle_name = middle_name
        self.age = age
        self.cls = cls
        self.id = id

        if id is not None:
            data = self.manager.get_member_data_by_id(id)
            if len(data) > 0:
                self.name = data[0][1]
                self.surname = data[0][2]
                self.middle_name = data[0][3]
                self.age = data[0][4]
                self.cls = data[0][5]
                self.in_db = True

    def __str__(self):
        return f"Кружковец {self.surname} {self.name} {self.middle_name}, {self.age} лет, {self.cls} с id {self.id}"

    def __repr__(self):
        return self.__str__()


class Lesson(TableItem):
    def __init__(self, manager, start="14:00:00", finish="16:00:00", day=1, teacher_id=None, group_id=None, group=None,
                 teacher=None, id=None):
        super().__init__(manager, id)
        self.group = group
        self.teacher = teacher
        self.start = start
        self.finish = finish
        self.day = day
        self.teacher_id = teacher_id
        self.group_id = group_id

        if id is not None:
            data = self.manager.get_lesson_data_by_id(id)
            print(data[0])
            if len(data) > 0:
                self.start = str(data[0][1])
                self.finish = str(data[0][2])
                self.day = data[0][3]
                self.teacher_id = data[0][4]
                self.group_id = data[0][5]
                self.in_db = True

        if self.group is not None:
            if self.group.in_db:
                if not self.in_db:
                    self.group_id = self.group.id
            else:
                self.group_id = None

        if self.teacher is not None:
            if self.teacher.in_db:
                if not self.in_db:
                    self.teacher_id = self.teacher.id
            else:
                self.teacher_id = None

    def __str__(self):
        return f"Урок с началом в '{self.start}' и окончанием '{self.finish}' дня '{self.day}', с id группы " \
               f"{self.group_id}, с id учителя {self.teacher_id} и id {self.id}"

    def __repr__(self):
        return self.__str__()


class Group(TableItem):
    def __init__(self, manager, name="Безямынная группа", club_id=None, id=None, club=None):
        super().__init__(manager, id)
        self.club = club
        self.lessons = []
        self.id = id
        self.name = name
        self.club_id = club_id

        if id is not None:
            data = self.manager.get_group_data_by_id(id)
            if len(data) > 0:
                self.name = data[0][1]
                self.club_id = data[0][2]
                self.in_db = True

        if self.club is not None:
            if self.club.in_db:
                if not self.in_db:
                    self.club_id = self.club.id
            else:
                self.club_id = None

    def add_lesson(self, start="14:00:00", finish="16:00:00", day=1, teacher_id=None, teacher=None, lesson=None):
        if lesson is None:
            lesson = Lesson(self.manager, start=start, finish=finish, day=day, teacher_id=teacher_id,
                            teacher=teacher,  group=self)
        else:
            lesson.club = self
        self.lessons.append(lesson)

    def insert(self, id):
        super().insert(id)
        for lesson in self.lessons:
            lesson.group_id = self.id
            self.manager.add_lesson(lesson=lesson)

    def __str__(self):
        return f"Группа '{self.name}' кружка с id {self.club_id}, с собственным id {self.id}"

    def __repr__(self):
        return self.__str__()


class Club(TableItem):
    def __init__(self, manager, name="Безымянный кружок", category=1, description="", id=None):
        super().__init__(manager, id)
        self.name = name
        self.category = category
        self.description = description
        self.groups = []
        self.id = id

        if id is not None:
            data = self.manager.get_club_data_by_id(id)
            if len(data) > 0:
                self.name = data[0][2]
                self.category = data[0][1]
                self.description = data[0][3]
                self.in_db = True

    def add_group(self, name="Безымянная группа", group=None):
        if group is None:
            group = Group(self.manager, name=name, club=self)
        else:
            group.club = self
        self.groups.append(group)

    def insert(self, id):
        super().insert(id)
        for group in self.groups:
            group.club_id = self.id
            self.manager.add_group(group=group)

    def __str__(self):
        return f"Кружок '{self.name}' из категории с номером '{self.category}', с описанием '{self.description}' и id {self.id}"

    def __repr__(self):
        return self.__str__()


class Manager:
    def __init__(self, db):
        self.db = db

    def add_club(self, name="Безымянный кружок", category=1, description="", club=None):  # Занести кружок в бд
        if club is not None:
            if club.in_db:
                return "-1"
            name, category, description = club.name, club.category, club.description
        query = f"INSERT INTO `club` (`name`, `category_id`, `description`) VALUES ('{name}', '{category}', '{description}')"
        self.db.query(query)
        # Получение id только что занесенного кружка
        query = "SELECT id FROM `club` WHERE 1 ORDER BY `id` DESC LIMIT 1"
        result = self.db.query(query)
        if club is not None:
            club.insert(result[0][0])
        return result

    def remove_club(self, club=None, club_id=None):
        if club is not None:
            if not club.in_db:
                return "-1"
            club_id = club.id
        query = f"DELETE FROM `club` WHERE `id` = {club_id}"
        self.db.query(query)
        query = f"SELECT `id` FROM `club_group` WHERE `club_id` = '{club_id}'"
        result = self.db.query(query)
        for group in result:
            group_id = group[0]
            print(group_id)
            query = f"DELETE FROM `club_group` WHERE `id` = {group_id}"
            self.db.query(query)
            query = f"DELETE FROM `club_group_lesson` WHERE `id` = {group_id}"
            self.db.query(query)
            query = f"DELETE FROM `club_group_member` WHERE `id` = {group_id}"
            self.db.query(query)

    def update_club(self, club=None, club_id=None):
        if club is not None:
            club_id = club.id
        name, category, description = club.name, club.category, club.description
        query = f"UPDATE `club` SET `name` = '{name}', `category_id` = '{category}', " \
                f"`description` = '{description}' WHERE `id` = '{club_id}'"
        self.db.query(query)

    def add_group(self, name="Безымянная группа", club_id=1, group=None):  # Занести кружок в бд
        if group is not None:
            if group.in_db or group.club_id is None:
                return "-1"
            name, club_id = group.name, group.club_id
        query = f"INSERT INTO `club_group` (`name`, `club_id`) VALUES ('{name}', '{club_id}')"
        self.db.query(query)
        # Получение id только что занесенного кружка
        query = "SELECT id FROM `club_group` WHERE 1 ORDER BY `id` DESC LIMIT 1"
        result = self.db.query(query)
        if group is not None:
            group.insert(result[0][0])
        return result

    def remove_group(self, group=None, group_id=None):
        if group is not None:
            if not group.in_db:
                return "-1"
            group_id = group.id
        query = f"DELETE FROM `club_group` WHERE `id` = {group_id}"
        self.db.query(query)
        query = f"DELETE FROM `club_group_lesson` WHERE `id` = {group_id}"
        self.db.query(query)
        query = f"DELETE FROM `club_group_member` WHERE `id` = {group_id}"
        self.db.query(query)

    def update_group(self, group=None, group_id=None):
        if group is not None:
            group_id = group.id
        name, club_id = group.name, group.club_id
        query = f"UPDATE `club_group` SET `name` = '{name}', `club_id` = '{club_id}' WHERE `id` = '{group_id}'"
        self.db.query(query)

    def add_lesson(self, start="14:00:00", finish="16:00:00", day=1, teacher_id=None, group_id=None, lesson=None):  #
        # Занести кружок в бд
        if lesson is not None:
            if lesson.in_db or lesson.group_id is None or lesson.teacher_id is None:
                return "-1"
            start, finish, day, teacher_id, group_id = lesson.start, lesson.finish, lesson.day, lesson.teacher_id, \
                                                       lesson.group_id
        query = f"INSERT INTO `club_group_lesson` ( `start`, `finish`, `day`, `teacher_id`, `group_id`) VALUES (" \
                f"'{start}', '{finish}', '{day}', '{teacher_id}', '{group_id}')"
        self.db.query(query)
        # Получение id только что занесенного кружка
        query = "SELECT id FROM `club_group_lesson` WHERE 1 ORDER BY `id` DESC LIMIT 1"
        result = self.db.query(query)
        if lesson is not None:
            lesson.insert(result[0][0])
        return result

    def remove_lesson(self, lesson=None, lesson_id=None):
        if lesson is not None:
            if not lesson.in_db:
                return "-1"
            lesson_id = lesson.id
        query = f"DELETE FROM `club_group_lesson` WHERE `id` = {lesson_id}"
        self.db.query(query)

    def update_lesson(self, lesson=None, lesson_id=None):
        if lesson is not None:
            lesson_id = lesson.id
        start, finish, day, teacher_id = lesson.start, lesson.finish, lesson.day, lesson.teacher_id
        query = f"UPDATE `club_group_lesson` SET `start` = '{start}', `finish` = '{finish}', `day` = '{day}', " \
                f"`teacher_id` = '{teacher_id}' WHERE " \
                f"`id` = " \
                f"'{lesson_id}'"
        self.db.query(query)

    def add_member(self, name="Иван", surname="Иванов", middle_name="Иванович", age=15, cls="9a", member=None):
        # Занести кружок в бд
        if member is not None:
            if member.in_db:
                return "-1"
            name, surname, middle_name, age, cls = member.name, member.surname, member.middle_name, member.age, \
                                                   member.cls
        query = f"INSERT INTO `club_member` ( `name`, `surname`, `middle_name`, `age`, `class`) VALUES (" \
                f"'{name}', '{surname}', '{middle_name}', '{age}', '{cls}')"
        self.db.query(query)
        # Получение id только что занесенного кружка
        query = "SELECT id FROM `club_member` WHERE 1 ORDER BY `id` DESC LIMIT 1"
        result = self.db.query(query)
        if member is not None:
            member.insert(result[0][0])
        return result

    def remove_member(self, member=None, member_id=None):
        if member is not None:
            if not member.in_db:
                return "-1"
            member_id = member.id
        query = f"DELETE FROM `club_member` WHERE `id` = '{member_id}'"
        self.db.query(query)
        query = f"DELETE FROM `club_group_member` WHERE `member_id` = '{member_id}'"
        self.db.query(query)

    def update_member(self, member=None, member_id=None):
        if member is not None:
            member_id = member.id
        name, surname, middle_name, age, cls = member.name, member.surname, member.middle_name, member.age, member.cls
        query = f"UPDATE `club_member` SET `name` = '{name}', `surname` = '{surname}', `middle_name` = '" \
                f"{middle_name}', " \
                f"`age` = '{age}', `cls` = '{cls}' WHERE " \
                f"`id` = " \
                f"'{member_id}'"
        self.db.query(query)

    def add_group_member(self, group_id=1, member_id=1, group_member=None):
        if group_member is not None:
            if group_member.in_db or group_member.group_id is None or group_member.member_id is None:
                return "-1"
            group_id, member_id = group_member.group_id, group_member.member_id
        query = f"INSERT INTO `club_group_member` ( `group_id`, `member_id`) VALUES ({group_id}, {member_id})"
        self.db.query(query)
        # Получение id только что занесенного кружка
        query = "SELECT id FROM `club_group_member` WHERE 1 ORDER BY `id` DESC LIMIT 1"
        result = self.db.query(query)
        if group_member is not None:
            group_member.insert(result[0][0])
        return result

    def remove_group_member(self, group_member=None, group_member_id=None):
        if group_member is not None:
            if not group_member.in_db:
                return "-1"
            group_member_id = group_member.id
        query = f"DELETE FROM `club_group_member` WHERE `id` = '{group_member_id}'"
        self.db.query(query)

    def add_user(self, type_id=1, name="Иван", surname="Иванов", middle_name="Иванович", description="",
                 login="login1", password="password", image="", user=None):
        if user is not None:
            if user.in_db:
                return "-1"
            type_id, name, surname, middle_name, login, password, image, description = user.type_id, user.name, \
                                                                                user.surname, user.middle_name, \
                                                                                user.login, user.password, \
                                                                                user.image, user.description
        query = f"INSERT INTO `user` (`type_id`, `name`, `surname`, `middle_name`, `login`, `password`, " \
                f"`description`, `image`) " \
                f"VALUES ('{type_id}', '{name}', '{surname}', '{middle_name}', '{login}', '{password}', " \
                f"'{description}', '{image}')"
        self.db.query(query)
        # Получение id только что занесенного кружка
        query = "SELECT id FROM `user` WHERE 1 ORDER BY `id` DESC LIMIT 1"
        result = self.db.query(query)
        if user is not None:
            user.insert(result[0][0])
        return result

    def remove_user(self, user=None, user_id=None):
        if user is not None:
            if not user.in_db:
                return "-1"
            user_id = user.id
        query = f"DELETE FROM `user` WHERE `id` = '{user_id}'"
        self.db.query(query)

    def update_user(self, user=None, user_id=None):
        if user is not None:
            user_id = user.id
        type_id, name, surname, middle_name, login, password, description, image = user.type_id, user.name, \
                                                                                 user.surname, \
                                                                            user.middle_name, user.login, \
                                                                            user.password, user.description, user.image
        query = f"UPDATE `user` SET `type_id` = '{type_id}', `name` = '{name}', `surname` = '{surname}', " \
                f"`middle_name` = '{middle_name}', `login` = '{login}', `password` = '{password}', `description` = '" \
                f"{description}', `image` = '{image}' WHERE `id` = '{user_id}'"
        self.db.query(query)

    def add_member_to_group(self, group=None, group_id=None, member=None, member_id=None):
        if member is not None:
            if not member.in_db:
                self.add_member(member=member)
        else:
            if member_id is None:
                return "-1"
            member = Member(self, id=member_id)

        if group is not None:
            if not group.in_db:
                self.add_group(group=group)
        else:
            if group_id is None:
                return "-1"
            group = Group(self, id=group_id)

        self.add_group_member(group_id=group.id, member_id=member.id)

    def add_club_category(self, name):
        query = f"INSERT INTO `club_category` (`name`) VALUES ('{name}')"
        self.db.query(query)

    def get_club_data_by_id(self, id):
        query = f"SELECT * FROM `club` WHERE `id` = '{id}'"
        result = self.db.query(query)
        return result

    def get_group_data_by_id(self, id):
        query = f"SELECT * FROM `club_group` WHERE `id` = '{id}'"
        result = self.db.query(query)
        return result

    def get_lesson_data_by_id(self, id):
        query = f"SELECT * FROM `club_group_lesson` WHERE `id` = '{id}'"
        result = self.db.query(query)
        return result

    def get_member_data_by_id(self, id):
        query = f"SELECT * FROM `club_member` WHERE `id` = '{id}'"
        result = self.db.query(query)
        return result

    def get_group_member_data_by_id(self, id):
        query = f"SELECT * FROM `club_group_member` WHERE `id` = '{id}'"
        result = self.db.query(query)
        return result

    def get_group_member_data_by_links(self, member_id=0, group_id=0):
        query = f"SELECT * FROM `club_group_member` WHERE `member_id` = '{member_id}' AND `group_id` = '{group_id}'"
        result = self.db.query(query)
        return result

    def get_user_data_by_id(self, id):
        query = f"SELECT * FROM `user` WHERE `id` = '{id}'"
        result = self.db.query(query)
        return result

    def get_user_type_by_type_id(self, id):
        query = f"SELECT `name` FROM `user_type` WHERE `id` = '{id}'"
        result = self.db.query(query)
        try:
            return result[0][0]
        except Exception:
            return "-1"

    def get_user_type_by_user_id(self, id):
        query = f"SELECT `name` FROM `user_type` WHERE `id` = (SELECT `type_id` FROM `user` WHERE `id` = '{id}')"
        result = self.db.query(query)
        try:
            return result[0][0]
        except Exception:
            return "-1"

    def get_club_category_by_category_id(self, id):
        query = f"SELECT `name` FROM `club_category` WHERE `id` = '{id}'"
        result = self.db.query(query)
        try:
            return result[0][0]
        except Exception:
            return "-1"

    def get_club_category_by_club_id(self, id):
        query = f"SELECT `name` FROM `club_category` WHERE `id` = (SELECT `category_id` FROM `club` WHERE `id` = '{id}')"
        result = self.db.query(query)
        try:
            return result[0][0]
        except Exception:
            return "-1"


db = DB()
manager = Manager(db)
"""member1 = Member(manager, name="Александр", surname="Лебедев", middle_name="Сергеевич")
member2 = Member(manager, name="Семен", surname="Громов", middle_name="Дмитриевич")
member3 = Member(manager, name="Юрий", surname="Бондарев", middle_name="Александрович")
manager.add_member(member=member1)
manager.add_member(member=member2)
manager.add_member(member=member3)
group = Group(manager, name="9 класс", club_id=1)
manager.add_member_to_group(member=member1, group=group)
manager.add_member_to_group(member=member2, group=group)
manager.add_member_to_group(member=member3, group=group)"""
"""admin = User(manager, name="Иван", surname="Иванов", middle_name="Сидорович", type_id=1, login="ivanov",
             password="ivanov123",
             description="Главный администратор")
manager.add_user(user=admin)"""
"""club = Club(manager, id=2)
club.name = "Шухматы"
manager.remove_club(club=club)"""
#db.commit()
#cl = clubs.add_club("Шахматы3", 1, "Шахматный клуб помогает классно прыгать конем")

#db.commit()