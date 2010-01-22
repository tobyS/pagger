import sys
import os
import os.path
import re

import config
import mp3.handler
import shell

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

        while len(mapped) < 1:
            cmd = shell.Shell(handler, self._config)
            cmd.cmdloop(
                'No tags mapped for "' + handler.get_title() + '" by "' + handler.get_artist() + '"'
            )
            mapped = self._map_tags(handler.get_tags())

        print mapped
        
    def _map_tags(self, tags):
        mapped = []
        for tag in tags:
            if tag.lower() in self._config.tagmap:
                mapped.append(self._config.tagmap[tag.lower()])
        return set(mapped)

