import sys
import os
import os.path

import config
import mp3.handler

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
        handler = mp3.handler.Handler(self._config)
        for root, dirs, files in os.walk(self._dir):
            for file in files:
                handler.handle(os.path.join(root, file))
