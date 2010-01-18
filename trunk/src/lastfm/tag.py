class Tag:
    name = ''
    url = ''
    count = -1

    def __init__(self, name, url, *params):
        self.name = name
        self.url = url
        if len(params) > 0:
            self.count = params[0]
