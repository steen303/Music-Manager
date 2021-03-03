from sqlite3 import Error
import logging

from app.db.database import create_connection, does_col_contain_val
from app.domain.playlist import Playlist, Playlists


# todo add triggers to database
class DbPlaylist:
    sql_contains_playlist_id = "SELECT count(ID) FROM yt_playlist WHERE ID LIKE :ID"
    sql_update = "UPDATE yt_playlist SET title = :title, description = :description, " \
                 "WHERE ID LIKE :ID"
    sql_insert = "INSERT OR REPLACE INTO yt_playlist (ID, title, description) " \
                 "VALUES (:ID, :title, :description)"

    def contains_playlist_with_id(self, playlist=Playlist(0)):
        return does_col_contain_val(self.sql_contains_playlist_id, "ID", playlist.ID)

    def update(self, playlist):
        try:
            conn, c = create_connection()
            c.execute(self.sql_update, {"title": playlist.title, "description": playlist.description,
                                        "ID": playlist.ID})
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            logging.warning("db: %s", e)

    def insert_playlist(self, playlist):
        try:
            conn, c = create_connection()
            c.execute(self.sql_insert,
                      {"ID": playlist.ID, "title": playlist.title, "description": playlist.description})
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
            logging.warning("db: %s", e)

    def insert_multiple_playlists(self, playlists):
        for playlist in playlists:
            self.insert_playlist(playlist)
