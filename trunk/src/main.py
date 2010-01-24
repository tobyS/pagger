import sys, traceback
import os
import os.path
import re

from config import Config
from mp3 import MP3
import handler.tags
from shell import Shell

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

        self._config = Config(sys.argv[1])
        self._dir = sys.argv[2]

    def run(self):
        for root, dirs, files in os.walk(self._dir):
            for file in files:
                try:
                    self._handle(os.path.join(root, file))
                except StandardError as e:
                    print u'Error processing "', file, u'". Error:', e, u' (', type(e), u')'
                    traceback.print_exc(file=sys.stdout)

    def _handle(self, file):
        mp3 = MP3(file)
        
        if mp3.is_processed():
            # Skip already processed MP3s
            # TODO: Add command line switch to ignore this and process anyway!
            return

        tag = handler.tags.Handler(self._config, mp3)

        if tag.has_unmapped_tags():
            unmapped = tag.get_unmapped_tags()
            cmd = Shell(self._config, mp3, tag)
            cmd.cmdloop(
                u'Unmapped tags mapped for "' + mp3.get_title() + u'" by "' + mp3.get_artist() + u'"'
            )

        if len(tag.get_tags()) == 0:
            cmd = shell.Shell(self._config, mp3, tag)
            cmd.cmdloop(
                u'No fitting tags found for "' + mp3.get_title() + u'" by "' + mp3.get_artist() + u'". Please assign manually!'
            )

        if self._config.changed():
            self._config.save()

        print u'Assigning genres "' + u', '.join(tag.get_tags()) + u'" to "' + mp3.get_title() + u'" by "' + mp3.get_artist() + u'".'

        mp3.set_genres(tag.get_tags())
        mp3.set_processed()
        mp3.save()
        
    def _map_tags(self, tags):
        mapped = []
        for tag in tags:
            if tag.lower() in self._config.tagmap:
                mapped.append(self._config.tagmap[tag.lower()])
        return set(mapped)

