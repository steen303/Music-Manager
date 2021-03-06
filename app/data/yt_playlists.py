import os

import googleapiclient.discovery

import sqlite3
from app.domain.playlist import Playlist, Playlists


class YtPlaylists:
    def __init__(self, channel_id="UC-Lxw-5-0PEFAKvH6g8MAcQ"):
        self.channel_id = channel_id
        self.items = Playlists(channel_id)
        self.get_from_youtube()

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
        self.items = self.create_playlists(response["items"])
        self.items = response["items"]

    def get_playlists(self):
        return self.items
        # TODO get playlists from database

    def create_playlist(self, id, title=None, description=None):
        playlist = Playlist(id, title, description)
        return playlist

    def create_playlists(self, respons_items):
        for item in respons_items:
            self.items.append(
                self.create_playlist(item["id"], item["snippet"]["title"], item["snippet"]["description"]))

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
