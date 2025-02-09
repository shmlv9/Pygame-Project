import sqlite3


def get_record(level):
    connection = sqlite3.connect('data/database/main_database.sqlite')
    cursor = connection.cursor()
    res = cursor.execute(f'''
    SELECT record FROM records
    WHERE level = "{level}"
    ''').fetchone()[0]
    return res


def update_record(level, record):
    connection = sqlite3.connect('data/database/main_database.sqlite')
    cursor = connection.cursor()
    cursor.execute(f'''
        UPDATE records
        SET record = "{record}"
        WHERE level = "{level}"
        ''')
    connection.commit()
    connection.close()
