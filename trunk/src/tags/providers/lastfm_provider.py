from base import Base
import re

import lastfm.service
import lastfm.artist
import lastfm.track

class LastFMProvider(Base):

    _service = None

    def __init__(self, config, mp3):
        Base.__init__(self, config, mp3)
        self._service = lastfm.service.Service()

    def retrieve_tags(self):
        artist = self._clean_string(self._mp3.get_artist())
        title = self._clean_string(self._mp3.get_title())

        tags = filter(self._filter_tags, self._fetch_title_tags(artist, title))

        if len(tags) == 0:
            tags = filter(self._filter_tags, self._fetch_artist_tags(artist))

        tags = map(self._extract_tags, tags)
        return set(tags)

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
        if tag.count > -1 and tag.count < self._config.settings['minScore']:
            return False
        for regex in self._config.ignore:
            if re.search(regex, tag.name):
                return False
        return True

    def _extract_tags(self, tag):
        return tag.name
