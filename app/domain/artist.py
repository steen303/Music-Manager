class Artist:
    def __init__(self, name, discogs_id=None, real_name=None, profile=None, url=None):
        self.ID = discogs_id
        self.name = name
        self.real_name = real_name
        self.profile = profile
        self.url = url

    def __repr__(self) -> str:
        return "Artist(%s, %s)" % (self.ID, self.name)

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.ID == other.ID and self.name == other.name
        else:
            return False
