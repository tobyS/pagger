import service
from mixins.tagparser import TagParser

class Artist (TagParser):

    _service = None

    name = ''

    def __init__(self, service, name):
        self._service = service
        self.name = name

    def get_top_tags(self):
        xml = self._service.call('artist', 'getTopTags', {'artist': self.name})
        return self.parse_tags(xml)
