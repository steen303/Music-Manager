from data.albums import Albums
from data.artists import Artists
import logging


class Songs:
    def __init__(self, songs):
        self.songs = songs

    def find_and_check_online_tags(self, q):
        self.find_artists_online()
        self.find_albums_online()
        print(q.get())
        q.task_done()

    def find_artists_online(self):
        logging.info('start searching for artists')
        artists = Artists()
        artists.extract_from_songs(self.songs)
        artists.search_online()
        logging.info('done searching for artists')

    def find_albums_online(self):
        logging.info('start searching for albums')
        albums = Albums()
        filtered_songs = albums.extract_from_songs(self.songs)
        albums.search_online(filtered_songs)
        sorted_alb = albums.sort_by_file_name()
        logging.info('done searching for albums')

    def link_tags_to_file(self, q):
        logging.info('start linking artists to files')
        Artists.link_to_files(self.songs)
        logging.info('done linking artists to files')
        print(q.get())
        q.task_done()
