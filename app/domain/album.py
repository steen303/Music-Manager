class MasterRelease:
    def __init__(self, title, discogs_id=None, year=None, url=None, main_release=None, ):
        self.ID = discogs_id
        self.title = title
        self.year = year
        self.url = url
        self.main_release = main_release

    def __repr__(self) -> str:
        return "Artist(%s, %s)" % (self.ID, self.title)

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.ID == other.ID and self.title == other.title
        else:
            return False


class Album:
    def __init__(self, title, discogs_id=None, master_id=None, country=None, release_year=None, year=None, url=None):
        self.ID = discogs_id
        if master_id is None:
            pass
        else:
            self.master_id = master_id
        self.title = title
        self.country = country
        self.release_year = release_year
        self.year = year
        self.url = url
        self._compilation = ''
        self._artist = ''

    def __repr__(self) -> str:
        return "Artist(%s, %s)" % (self.ID, self.title)

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.ID == other.ID and self.title == other.title
        else:
            return False

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = value

    @property
    def compilation(self):
        return self._compilation

    @compilation.setter
    def compilation(self, value):
        self._compilation = value
