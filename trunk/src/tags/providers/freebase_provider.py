from base import Base

import urllib
import json
import xml.sax.saxutils as saxutils 

class FreebaseProvider (Base):

    _base_url = u"http://api.freebase.com/api/service/mqlread?query="

    _config = None
    
    _mp3 = None

    def retrieve_tags(self):
        return self._process(self._query(self._mp3.get_artist()))

    def _query(self, artist):
        query = {
            u"query": [
                {
                    u"/type/object/name": artist,
                    u"/type/object/type": u"/music/artist",
                    u"/music/artist/genre": [{}]
                }
            ]
        }
        return urllib.urlopen(
            self._base_url + urllib.quote(json.dumps(query))
        ).read()

    def _process(self, encoded):
        decoded = json.loads(encoded)
        if decoded["code"] != "/api/status/ok":
            raise RuntimeError("Freebase query failed")
        if decoded["status"] != "200 OK":
            return set()
        return set(map(
            lambda genre: saxutils.unescape(genre["name"]),
            decoded["result"][0]["/music/artist/genre"]
        ))
