import sqlite3


def setup_device():
    connection = sqlite3.connect("shscamera")

    cursor = connection.cursor()

    sql_file = open("databaseinit.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
    connection.commit()
    cursor.close()
    connection.close()
    print("setup complete!")
