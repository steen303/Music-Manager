import itertools
import pathlib
import sqlite3
from sqlite3 import Error

from app.conf.configurator import get_value
from app.db.statements import Statements as Stmt
import logging


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


# artist
# def add_artist(id_val, name, real_name, url, profile, group, groupmember):
#     try:
#         conn, c = create_connection()
#         c.execute("SELECT count(name) FROM artist WHERE name like :name ", {"name": name})
#         if c.fetchone()[0] < 1:
#             query = '''INSERT INTO artist ('id', name, real_name, url, profile, 'group', groupmember)
#                 VALUES (?, ?, ?, ?, ?, ?, ?)'''
#             c.execute(query, (id_val, name, real_name, url, profile, group, groupmember))
#             # self.conn.commit()
#         conn.close()
#     except Error as e:
#         print(e)


# file_artist
# def file_artist_add(name, discogs_name, discogs_id):
#     try:
#         conn, c = create_connection()
#         if file_artist_exist(name):
#             c.execute(Stmt.file_artist_add, (name, discogs_name, discogs_id))
#             c.execute(Stmt.file_artist_confirm)
#             conn.commit()
#         conn.close()
#     except Error as e:
#         print(e)


def file_artist_add_multiple(tags):
    try:
        conn, c = create_connection()
        c.executemany(Stmt.file_artist_add, tags)
        c.execute(Stmt.file_artist_confirm)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
        logging.warning("db: %s", e)


def file_artist_exist(name):
    return does_col_contain_val(Stmt.file_artist_exist, 'name', name)


def file_artist_names_get_all():
    try:
        conn, c = create_connection()
        c.execute(Stmt.file_artist_get_all)
        file_artist_names = set()
        rows = c.fetchall()
        conn.close()
        for row in rows:
            file_artist_names.add(row[0])
        return file_artist_names
    except Error as e:
        print(e)
        logging.warning("db: %s", e)


# file_artist_location
def file_artist_location_add_multiple(tags):
    try:
        conn, c = create_connection()
        c.executemany(Stmt.file_artist_location_add, tags)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
        logging.warning("db: %s", e)


# location
# def location_add(path):
#     try:
#         conn, c = create_connection()
#         c.execute(Stmt.location_add, (path, 0))
#         conn.commit()
#         conn.close()
#     except Error as e:
#         print(e)


def location_add_multiple(paths):
    try:
        conn, c = create_connection()
        query = Stmt.location_add
        c.executemany(query, paths)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
        logging.warning("db: %s", e)


def location_exists(path):
    return does_col_contain_val(Stmt.location_exists, "path", path)


# def location_get_first():
#     try:
#         conn, c = create_connection()
#         c.execute(Stmt.location_get_first)
#         loc = c.fetchone()[0]
#         c.close()
#         return loc
#     except Error as e:
#         print(e)


def location_get_all():
    try:
        conn, c = create_connection()
        c.execute(Stmt.location_get_all)
        file_list = list(itertools.chain.from_iterable(c.fetchall()))
        conn.close()
        files = []
        for f in file_list:
            files.append(pathlib.Path(f))
        return files
    except Error as e:
        print(e)
        logging.warning("db: %s", e)


# :: release ::


# file_release
# todo add triggers to database
def enable_check_tag_artist(check_title, check_year, check_artist, check_tracks, title):
    try:
        conn, c = create_connection()
        c.execute(Stmt.enable_check_tag_artist, {"check_title": check_title, "check_year": check_year,
                                                 "check_artist": check_artist, "check_tracks": check_tracks,
                                                 "title": title})
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
        logging.warning("db: %s", e)


def check_tag_release(title):
    return does_col_contain_val(Stmt.file_release_exists, "title", title)


def insert_tag_album(title, discogs_title, discogs_id, year, compilation):
    try:
        conn, c = create_connection()
        c.execute(Stmt.sql_insert_release,
                  {"title": title, "discogs_title": discogs_title, "discogs_id": discogs_id, "year": year,
                   "compilation": compilation})
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
        logging.warning("db: %s", e)


def confirm_check_tag_artist():
    try:
        conn, c = create_connection()
        c.execute(Stmt.confirm_release)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
        logging.warning("db: %s", e)
