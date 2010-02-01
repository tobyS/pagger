class Base:

    _config = None

    _mp3 = None

    def __init__(self, config, mp3):
        self._config = config
        self._mp3 = mp3

    def retriev_tags(self):
        return set()
