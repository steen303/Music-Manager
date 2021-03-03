from sqlite3 import Error
import logging

from data.util.sqlite_connection import create_connection, does_col_contain_val
from domain.artist import Artist


class SqliteFileArtist:
    file_artist_add = "INSERT OR IGNORE INTO file_artist (name, discogs_name, discogs_id) " \
                      "VALUES (:tag_name, :name, :id)"
    sql_file_artist_confirm = "UPDATE file_artist set confirmed = 1 WHERE name LIKE discogs_name"
    sql_file_artist_exist = "SELECT count(name) FROM file_artist WHERE name LIKE :name ORDER BY name ASC "
    sql_file_artist_get_all = "SELECT name FROM file_artist ORDER BY name ASC"

    def add_multiple(self, tags):
        try:
            conn, c = create_connection()
            c.executemany(self.file_artist_add, tags)
            c.execute(self.sql_file_artist_confirm)
            # todo add trigger to db
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            logging.warning("db: %s", e)

    def exists(self, name):
        return does_col_contain_val(self.sql_file_artist_exist, 'name', name)

    def get_all_names(self):
        try:
            conn, c = create_connection()
            c.execute(self.sql_file_artist_get_all)
            file_artist_names = set()
            rows = c.fetchall()
            conn.close()
            for row in rows:
                file_artist_names.add(row[0])
            return file_artist_names
        except Error as e:
            print(e)
            logging.warning("db: %s", e)

    def get_artists_set(self):
        artist_set = set()
        artists_names_in_db = self.get_all_names()
        for name in artists_names_in_db:
            artist_set.add(Artist(name))
        return artist_set
