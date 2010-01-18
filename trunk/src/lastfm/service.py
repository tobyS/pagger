
import urllib

class Service:
	_api_key = ""

	_base_url = u"http://ws.audioscrobbler.com/2.0/"

	def __init__(self, api_key):
		self._api_key = api_key


	def call(self, class_name, method_name, params):
		params['method'] = class_name + '.' + method_name
		params['api_key'] = self._api_key
		return urllib.urlopen(
			self._base_url + '?' + urllib.urlencode(params)
		).read()
