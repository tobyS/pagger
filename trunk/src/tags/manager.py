import lastfm.service
import lastfm.artist
import lastfm.track

import re

class Manager:

    _providers = []

    _config = None

    _raw_tags = set()

    _tag_mapping = {}

    def __init__(self, config, providers):
        self._providers = providers
        self._config = config

    def retrieve(self):
        for provider in self._providers:
            self._raw_tags |= provider.retrieve_tags()
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
        return len(self.get_unmapped_tags()) != 0

    def get_unmapped_tags(self):
        return self._raw_tags - set(self._tag_mapping.keys())

    def get_raw_tags(self):
        return self._raw_tags

    def _map_tags(self):
        for tag in self.get_unmapped_tags():
            if tag.lower() in self._config.tagmap:
                self._tag_mapping[tag] = self._config.tagmap[tag.lower()]

