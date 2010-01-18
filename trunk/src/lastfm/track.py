import service
from mixins.tagparser import TagParser

class Track (TagParser):

    _service = None

    artist = None

    title = ''

    def __init__(self, service, artist, title):
        self._service = service
        self.artist = artist
        self.title = title

    def get_top_tags(self):
        return self.parse_tags(
            self._service.call(
                'track',
                'getTopTags',
                {'artist': self.artist.name, 'track': self.title}
            )
        )
