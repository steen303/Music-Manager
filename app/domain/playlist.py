class Playlist:
    def __init__(self, playlist_id, title=None, description=None):
        self.ID = playlist_id
        self.title = title
        self.description = description

    def __repr__(self) -> str:
        return "Playlist(%s, %s)" % (self.ID, self.title)

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.ID == other.ID and self.title == other.title
        else:
            return False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self.description

    @description.setter
    def description(self, value):
        self.description = value


class Playlists:
    def __init__(self, channel_id=None, playlists=None):
        self.channel_id = channel_id
        if playlists is None:
            playlists = []
        self.playlists = playlists

    def __sizeof__(self) -> int:
        return len(self.playlists)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            is_equal = True
            for i in range(len(self.playlists)):
                is_equal = is_equal and self.playlists[i].ID == other.playlists[i].ID \
                           and self.playlists[i].title == other.playlists[i].title
            return is_equal
        else:
            return False

    def add_playlist(self, playlist):
        self.playlists.append(playlist)

    def sort(self):
        self.playlists.sort(key=self.take_id)

    @staticmethod
    def take_id(elem):
        return elem.ID


