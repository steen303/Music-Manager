import logging
from db import database as db
from domain.artist import Artist
from tags.tag_online import DiscogsTagger as Discogs
from data.sqlite_artist import SqliteFileArtist

ds = Discogs()


class Artists:
    def __init__(self):
        # todo replace with artist objects
        self.artists = []
        self.artist_names = set()

    def get_artists_from_db(self):
        artist_set = set()
        artists_names_in_db = db.file_artist_names_get_all()
        # totest new bolow
        # artists_names_in_db = SqliteFileArtist.file_artist_names_get_all()
        for name in artists_names_in_db:
            artist_set.add(Artist(name))
        return artist_set

    def extract_from_songs(self, songs):
        # artists_in_db = self.get_artists_from_db()
        artists_in_db = SqliteFileArtist.get_artists_set()
        artists_not_in_db = set()
        # totest test if extract still works
        # artists_names_in_db = db.file_artist_names_get_all()
        for song in songs:
            if "&" not in song.artist:
                artist = Artist(song.artist)
                artists_not_in_db.add(artist)
                # self.artist_names.add(song.artist)
        # self.artist_names.difference_update(artists_names_in_db)
        artists_not_in_db.difference_update(artists_in_db)

    def search_online(self):
        artists_tags = []
        for a in sorted(self.artists, key=lambda x: x.name, reverse=True):
            # totest remove print
            logging.debug("Artist: %s", a.name)
            tag_name, online_name, online_id = ds.get_artist(a.name)
            if online_name != '' and online_id != '':
                tag = {'tag_name': tag_name, 'name': online_name, 'id': online_id}
                artists_tags.append(tag)
        db.file_artist_add_multiple(artists_tags)

    @staticmethod
    def link_to_files(songs):
        # totest is it necessary to store artist location files
        tags = []
        for song in songs:
            if db.file_artist_exist(song.artist) and db.location_exists(song.location):  # and db.location_exists
                t = {'path': song.location, 'artist': song.artist}
                tags.append(t)
        db.file_artist_location_add_multiple(tags)

    def get_information(self):
        pass
        # todo get existing artists from artist table
        # todo substract existing artists from artist_names
        # todo iterate artists and get more information
        # todo store artists
