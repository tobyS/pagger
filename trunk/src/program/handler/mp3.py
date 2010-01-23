from mutagen.id3 import ID3
from mutagen.id3 import TCON

class Handler:

    _file = None

    _id3 = None

    _title = None

    _artist = None

    def __init__(self, file):
        self._file = file
        self._id3 = ID3(file)

    def get_title(self):
        if self._title != None:
            return self._title
        titles = self._id3.getall('TIT2')
        if len(titles) > 0:
            return str(titles[0])
        else:
            return ''

    def get_artist(self):
        if self._artist != None:
            return self._artist
        artists = self._id3.getall('TPE1')
        if len(artists) > 0:
            return str(artists[0])
        else:
            return ''

    def get_file(self):
        return self._file

    def set_genres(self, genres):
        self._id3['TCON'] = TCON(3, list(genres))

    def save(self):
        self._id3.save()
