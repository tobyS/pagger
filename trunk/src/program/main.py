import sys
import os
import os.path
import re

import config
import mp3.handler
import dialog.

class Main:

    _config = None

    _dir = ''

    def __init__(self):
        if len(sys.argv) < 2:
            raise RuntimeError('Missing argiment #1: Config file')
        if len(sys.argv) < 3:
            raise RuntimeError('Missing argument #2: Directory with MP3s')
        if not os.path.isfile(sys.argv[1]):
            raise RuntimeError(sys.argv[1] + ' is not a file')
        if not os.path.isdir(sys.argv[2]):
            raise RuntimeError(sys.argv[2] + ' is not a directory')

        self._config = config.Config(sys.argv[1])
        self._dir = sys.argv[2]

    def run(self):
        for root, dirs, files in os.walk(self._dir):
            for file in files:
                self._handle(os.path.join(root, file))

    def _handle(self, file):
        handler = mp3.handler.Handler(self._config, file)
        tags = handler.get_tags()
        mapped = self._map_tags(tags)

        if len(mapped) < 1 and len(tags) > 0:
            dialog = NewMapDialog(config, tags)
            mapped = dialog.get_result()
        elif len(mapped) < 1:
            dialog = CustomTagsDialog(config)
            mapped = dialog.get_result()

        print mapped
        
    def _map_tags(self, tags):
        mapped = []
        for tag in tags:
            if tag.lower() in self._config.tagmap:
                mapped.append(self._config.tagmap[tag.lower()])
        return set(mapped)

