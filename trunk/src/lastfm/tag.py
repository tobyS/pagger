class Tag:
    name = ''
    url = ''
    count = -1

    def __init__(self, name, url, *params):
        self.name = name
        self.url = url
        if len(params) > 0:
            self.count = params[0]

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Tag( name: ' + self.name + ', url: ' + self.url + ', count: ' + str(self.count) + ')>'
