import logging
from operator import attrgetter

from db import database as db
from tags.tag_online import DiscogsTagger as Discogs

ds = Discogs()


class Albums:
    # todo add search for file name, sort and find alg..
    # todo replace db with sqlite repo
    def __init__(self):
        # todo replace with album objects
        # self.albums = set()
        self.albumsObj = []

    def sort_by_file_name(self):
        return sorted(self.albumsObj, key=attrgetter('offline_title'))

    def extract_from_songs(self, songs):
        new_songs = []
        for song in songs:
            if self.search_album_with_name(song.album) is not None or db.check_tag_release(song.album):
                continue

            album = Album(song.album)
            album.year = song.year
            album.artist = song.artist
            self.albumsObj.append(album)

            new_songs.append(song)
        return new_songs

    @staticmethod
    def search_online(songs):
        for s in songs:
            tag_albumname, title, release_id, year, artist = ds.get_album(s)
            logging.debug(title + " :: " + tag_albumname)
            if title != '' or release_id != '' or year != '':
                # todo add all albums in one time to db
                db.insert_tag_album(tag_albumname, title, release_id, year, s.compilation)
                db.enable_check_tag_artist((s.album == title),
                                           int(str(s.year) == str(year)),
                                           (s.artist == artist), 0, tag_albumname)
            # todo albums found with all tags (name, artist, year) are authorized and kan be moved from tag
            # table to the real stuff and get a check on the confirmed collon in the table
        db.confirm_check_tag_artist()

    def search_album_with_name(self, name):
        # album = ""
        for alb in self.albumsObj:
            if name == alb.offline_title:
                # album = alb
                return alb
        else:
            # album = None
            return None
        # return album


class Album:
    def __init__(self, file_title, online_title='', online_id=''):
        self.offline_title = file_title
        self.online_id = online_id
        self.online_title = online_title
        self._compilation = ''
        self._artist = ''
        self._releaseyear = None
        self._year = ''
        self._country = None
        self._url = None

    def __repr__(self):
        return repr((self.offline_title, self.online_title, self.online_id))

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def compilation(self):
        return self._compilation

    @compilation.setter
    def compilation(self, value):
        self._compilation = value

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        self._country = value
