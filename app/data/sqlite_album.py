from sqlite3 import Error
import logging

from data.util.sqlite_connection import create_connection, does_col_contain_val
from domain.album import Album


# todo add triggers to database
class SqliteFileAlbum:
    # todo column congirmed and
    sql_insert = "INSERT INTO file_release (title, discogs_title, discogs_id, year, compilation) " \
                 "VALUES (:title, :discogs_title, :discogs_id, :year, :compilation)"
    sql_check_tags = "UPDATE file_release SET check_title = :check_title, check_year = :check_year, " \
                     "check_artist = :check_artist, check_tracks = :check_tracks " \
                     "WHERE title LIKE :title"
    sql_exists = "SELECT count(title) FROM file_release WHERE title LIKE :title"
    sql_confirm_release = "UPDATE file_release set confirmed = 1 where check_artist = 1 and check_year =1 " \
                      "and check_title = 1"

    def set_check_tags(self, check_title, check_year, check_artist, check_tracks, title):
        try:
            conn, c = create_connection()
            c.execute(self.sql_check_tags, {"check_title": check_title, "check_year": check_year,
                                            "check_artist": check_artist, "check_tracks": check_tracks,
                                            "title": title})
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            logging.warning("db: %s", e)

    def contains_title(self, title):
        return does_col_contain_val(self.sql_exists, "title", title)

    def insert_album(self, title, discogs_title, discogs_id, year, compilation):
        try:
            conn, c = create_connection()
            c.execute(self.sql_insert,
                      {"title": title, "discogs_title": discogs_title, "discogs_id": discogs_id, "year": year,
                       "compilation": compilation})
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            logging.warning("db: %s", e)
