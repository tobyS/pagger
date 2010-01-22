from mutagen.id3 import ID3

import lastfm.service
import lastfm.artist
import lastfm.track

import re

# import lastfm.service
# import lastfm.artist
# import lastfm.track

class Handler:

    _file = None

    _id3 = None

    _config = None

    _service = lastfm.service.Service()

    _title = None

    _artist = None

    _tags = None

    def __init__(self, config, file):
        self._config = config
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

    def get_tags(self):
        if self._tags != None:
            return self._tags

        artist = self._clean_string(self.get_artist())
        title = self._clean_string(self.get_title())

        tags = filter(self._filter_tags, self._fetch_title_tags(artist, title))

        if len(tags) == 0:
            tags = filter(self._filter_tags, self._fetch_artist_tags(artist))

        tags = map(self._extract_tags, tags)
        self._tags = set(tags)
        return self._tags

    def add_tag(self, tag):
        if self._tags == None:
            self.get_tags()
        self._tags.add(tag)

    def _clean_string(self, string):
        return re.sub('\(.*$', '', string)

    def _fetch_title_tags(self, artist, title):
        artist = lastfm.artist.Artist(self._service, artist)
        track = lastfm.track.Track(self._service, artist, title)
        return track.get_top_tags()

    def _fetch_artist_tags(self, artist):
        artist = lastfm.artist.Artist(self._service, artist)
        return artist.get_top_tags()

    def _filter_tags(self, tag):
        if tag.count < -1 or tag.count >= self._config.settings['minScore']:
            return True
        return False

    def _extract_tags(self, tag):
        return tag.name

