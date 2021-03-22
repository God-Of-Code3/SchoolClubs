import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


"""connection = create_connection("141.8.194.42", "a0286951_school-clubs", "umfx1113442006RIMERNICK",
                               "a0286951_school-clubs")"""
"""cursor = connection.cursor()
try:
    cursor.execute("SELECT * FROM `club`")
    result = cursor.fetchall()
    print(result)
except Error as e:
    print("error")"""