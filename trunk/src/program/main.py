import sys
import os
import os.path
import re

import config
import handler.mp3
import handler.tags
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
        mp3 = handler.mp3.Handler(file)
        tag = handler.tags.Handler(self._config, mp3)

        if tag.has_unmapped_tags():
            unmapped = tag.get_unmapped_tags()
            cmd = shell.Shell(self._config, mp3, tag)
            cmd.cmdloop(
                'Unmapped tags mapped for "' + mp3.get_title() + '" by "' + mp3.get_artist() + '"'
            )

        if self._config.changed():
            self._config.save()

        print 'Assigning genres "' + ', '.join(tag.get_tags()) + '" to "' + mp3.get_title() + '" by "' + mp3.get_artist() + '".'

        mp3.set_genres(tag.get_tags())
        mp3.save()
        
    def _map_tags(self, tags):
        mapped = []
        for tag in tags:
            if tag.lower() in self._config.tagmap:
                mapped.append(self._config.tagmap[tag.lower()])
        return set(mapped)

