# import sys
# import discogs_client
# from discogs_client.exceptions import HTTPError
from .discogs_authentication import authenticate

token = "LpYGwMzazdfdxAHCTRZhStSPMeyEVGNMYynuACzD"


class DiscogsTagger:
    def __init__(self):
        self.ds = authenticate()

    def get_artist(self, artist_tag):
        results = self.ds.search(artist_tag, type='artist')
        # totest test
        if results:
            artist = results[0]
            return artist_tag, artist.name, artist.id
        return artist_tag, '', ''

    def get_album(self, song, search_method=3):
        album_tag = song.album

        if search_method == 2:
            results = self.ds.search(song.album, type='release', artist=song.artist, year=song.year)
        elif search_method == 1:
            results = self.ds.search(song.album, type='release', artist=song.artist)
        else:
            results = self.ds.search(song.album, type='release', year=song.year)

        # totest test
        if results:
            release_id, title, year, artist = self.album_result_to_val(results[0])
            return song.album, title, release_id, year, artist.name
        elif 0 < search_method <= 2:
            search_method = search_method - 1
            self.get_album(song, search_method)
        return album_tag, '', '', '', ''

    def album_result_to_val(self, results):
        release_id = results.id
        release = self.ds.release(release_id)
        title = release.title
        year = release.year
        artist = release.artists[0]
        return release_id, title, year, artist
