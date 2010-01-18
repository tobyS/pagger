from mutagen.id3 import ID3

import lastfm.service
import lastfm.artist
import lastfm.track

class Handler:

    _config = None

    def __init__(self, config):
        self._config = config

    def handle(self, file):
        if not file[-4:] == '.mp3':
            return
        # artist, title = self._read_id3(file)
        self._read_id3(file)

    def _read_id3(self, file):
        id3 = ID3(file)

        titles = id3.getall('TIT2')
        artists = id3.getall('TPE1')
        title = titles[0] if len(titles) > 0 else ''
        artist = artists[0] if len(artists) > 0 else ''

        print file
        self._lookup_tags(artist, title)

    def _lookup_tags(self, artist, title):
        service = lastfm.service.Service('682587831457dcf13f569c79b930d866')
        artist = lastfm.artist.Artist(service, artist)
        track = lastfm.track.Track(service, artist, title)
        for tag in self._filter_tags(track.get_top_tags()):
            print u'    ' + tag.name + u' (' + tag.url + u') = ' + str(tag.count)
        

    def _filter_tags(self, tags):
        newtags = []
        i = 0
        for tag in tags:
            i = i + 1
            if tag.count == -1 or tag.count > self._config.settings['minScore']:
                newtags.append(tag)
            if i > self._config.settings['maxNum']:
                break
        return newtags


