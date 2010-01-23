import lastfm.service
import lastfm.artist
import lastfm.track

import re

class Handler:

    _mp3 = None

    _config = None

    _service = None

    _raw_tags = None

    _tag_mapping = {}

    def __init__(self, config, mp3):
        self._config = config
        self._mp3 = mp3
        self._service = lastfm.service.Service()

        self._retrieve_tags()
        self._map_tags()

    def add_tag(self, tag):
        self._raw_tags.add(tag)

    def remove_tag(self, tag):
        self._raw_tags.discard(tag)

    def get_raw_tags(self):
        return self._raw_tags

    def get_tags(self):
        if self.has_unmapped_tags():
            self._map_tags()
        return set(self._tag_mapping.values())

    def get_tag_mapping(self):
        if self.has_unmapped_tags():
            self._map_tags()
        return self._tag_mapping

    def has_unmapped_tags(self):
        return self._raw_tags != set(self._tag_mapping.values())

    def get_unmapped_tags(self):
        return self._raw_tags - set(self._tag_mapping.values())

    def get_raw_tags(self):
        return self._raw_tags

    def _map_tags(self):
        self._tag_mapping = {}
        for tag in self._raw_tags:
            if tag.lower() in self._config.tagmap:
                self._tag_mapping[tag] = self._config.tagmap[tag.lower()]

    def _retrieve_tags(self):
        artist = self._clean_string(self._mp3.get_artist())
        title = self._clean_string(self._mp3.get_title())

        tags = filter(self._filter_tags, self._fetch_title_tags(artist, title))

        if len(tags) == 0:
            tags = filter(self._filter_tags, self._fetch_artist_tags(artist))

        tags = map(self._extract_tags, tags)
        self._raw_tags = set(tags)

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
        if tag.count < 0 or tag.count >= self._config.settings['minScore']:
            return True
        return False

    def _extract_tags(self, tag):
        return tag.name
