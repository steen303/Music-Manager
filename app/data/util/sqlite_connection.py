import sqlite3
from sqlite3 import Error

from conf.configurator import get_value


def create_connection():
    try:
        conn = sqlite3.connect(get_value('database', 'dbFileLocation'))
        c = conn.cursor()
        return conn, c
    except Error as e:
        print(e)
    return None


def does_col_contain_val(statement: object, col: object, value: object) -> object:
    try:
        conn, c = create_connection()
        c.execute(statement, {col: value})
        value_found = (c.fetchone()[0] >= 1)
        c.close()
        return value_found
    except Error as e:
        print(e)