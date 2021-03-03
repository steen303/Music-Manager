import logging
from operator import attrgetter

from app.db import database as db

import os
import googleapiclient.discovery
import sqlite3


class SqlPlaylists:
    def __init__(self, ):
        self.playlists = []
        self.channel_id = channel_id
        self.items = []

    @staticmethod
    def get_from_youtube(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        developer_key = "AIzaSyApDD-ZgnAZcUnQnwPtnR2ztqk3H1IANag"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=developer_key)

        request = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=self.channel_id,
            maxResults=100
        )
        response = request.execute()

        print(response)
        self.items = response["items"]

    def get_from_db(self):
        pass
        # TODO get playlists from database

    def store_in_db(self):
        conn = sqlite3.connect('database.sqlite')
        for item in self.items:
            conn.execute("insert or replace into playlists (ID,Title,Description) values (?, ?, ?)",
                         (item["id"], item["snippet"]["title"], item["snippet"]["description"]))

        conn.commit()
        conn.close()

    def output(self):
        print(self.items)
        for item in self.items:
            print()
            print(item["id"])
            print(item["snippet"]["title"])


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
