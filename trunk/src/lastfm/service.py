import urllib

class Service:
    _api_key = '682587831457dcf13f569c79b930d866'

    _base_url = u'http://ws.audioscrobbler.com/2.0/'

    def call(self, class_name, method_name, params):
        params['method'] = class_name + '.' + method_name
        params['api_key'] = self._api_key
        return urllib.urlopen(
            self._base_url + '?' + urllib.urlencode(params)
        ).read()
