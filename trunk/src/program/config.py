from xml.dom.minidom import parse

class Config:

    settings = {
        'minScore': 80,
        'maxNum': 3
    }

    _available_settings = {
        'minScore': int,
        'maxNum': int
    }

    tags = set()

    tagmap = {}

    def __init__(self, file):
        self.load_file(file)

    def load_file(self, file):
        dom = parse(file)
        self._parse_settings(dom.getElementsByTagName('settings').item(0))
        self._parse_tags(dom.getElementsByTagName('tags').item(0))
        self._parse_tagmap(dom.getElementsByTagName('tagmap').item(0))

    def _parse_settings(self, settings):
        for node in settings.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                name = node.tagName
                self.settings[name] = self._available_settings[name](node.firstChild.nodeValue)
    
    def _parse_tags(self, tags):
        for node in tags.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
				tag = node.firstChild.nodeValue.strip()
                self.tags.add(tag)
				self.tagmap[tag.lower()] = tag
    
    def _parse_tagmap(self, tagmap):
        for node in tagmap.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                from_val = node.getElementsByTagName('from').item(0).firstChild.nodeValue.strip()
                to_val = node.getElementsByTagName('to').item(0).firstChild.nodeValue.strip()
                self.tagmap[from_val.lower()] = to_val
