import pathlib

import mutagen.mp3 as mp3
from mutagen.flac import FLAC

from conf import configurator as conf
from db import database as db


# todo move scan and store functions to another file
def scan_files_and_store():
    files = scan_files()
    store_files(files)
    return files


def scan_files():
    files = []
    folder = conf.get_value('music-library', 'artist-albums-dir')
    files = scan_directory(folder, files, False)
    return files


def scan_directory(startfolder, files, already_scanned):
    folder = pathlib.Path(startfolder)
    for f in folder.iterdir():
        if f.is_dir():
            scan_directory(f, files, False)
        elif not already_scanned:
            files.append(f)
            already_scanned = db.location_exists(str(f)) and not conf.get_boolean('music-library', 'run_filescan')
    return files


def store_files(files):
    files_path = []
    for file in files:
        files_path.append((str(pathlib.PurePath(file)), 0))
    db.location_add_multiple(files_path)


def read_tags_trom_files(files):
    tagged_songs = []
    for f in files:
        if f.suffix == '.mp3' or f.suffix == '.flac':
            s = MusicFile(f)
            s.add_tags()
            tagged_songs.append(s)
    return tagged_songs


class MusicFile:
    def __init__(self, location):
        self.filename = location.title
        self.extension = location.suffix
        self.location = str(location)
        self.album = ''
        self.artist = ''
        self.compilation = ''
        self.genre = []
        self.length = ''
        self.title = ''
        self.year = ''
        self.track = ''

    def add_tags(self):
        if self.extension == ".mp3":
            self.add_tags_mp3()
        elif self.extension == ".flac":
            self.add_tags_flac()

    def add_tags_mp3(self):
        audio = mp3.EasyMP3(self.location).tags
        self.album = audio['album'][0] if 'album' in audio else ''
        self.artist = audio['artist'][0] if 'artist' in audio else ''
        self.genre = audio['genre'] if 'genre' in audio else ''
        self.title = audio['title'][0] if 'title' in audio else ''
        self.year = audio['date'][0] if 'date' in audio else ''
        # todo bug fix compilation
        if 'compilation' in audio:
            self.compilation = audio['compilation'][0]

    def add_tags_flac(self):
        audio = FLAC(self.location).tags

        self.album = audio['album'][0] if 'album' in audio else ''
        self.artist = audio['artist'][0] if 'artist' in audio else ''
        self.genre = audio['genre'] if 'genre' in audio else ''
        self.title = audio['title'][0] if 'title' in audio else ''
        if 'date' in audio:
            self.year = audio['date'][0]
        if 'tracknumber' in audio:
            self.track = audio['tracknumber'][0]
        # todo bug fix compilation
        if 'compilation' in audio:
            self.compilation = audio['compilation'][0]
