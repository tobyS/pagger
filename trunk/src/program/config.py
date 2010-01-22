from xml.dom.minidom import parse
from xml.dom.minidom import getDOMImplementation

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

    def add_tag(self, tag):
        self.tags.add(tag)
        self.tagmap[tag.lower()] = tag

    def add_mapping(self, from_tag, to_tag):
        self.tagmap[from_tag.lower()] = to_tag

    def set(self, key, val):
        if key not in self._available_settings:
            raise RuntimeError('Invalid setting "' + key + '".')
        self.settings[key] = self._available_settings[key](val)

    def save(self, file):
        impl = getDOMImplementation()
        xml = impl.createDocument(None, 'config', None)
        config_elem = xml.documentElement

        settings_elem = config_elem.appendChild(xml.createElement('settings'))
        for key, val in self.settings:
            setting_elem = settings_elem.appendChild(xml.createElement(key))
            setting_elem.appendChild(xml.createTextNode(val))

        tags_elem = config_elem.appendChild(xml.createElement('tags'))
        for tag in self.tags:
            tag_elem = tags_elem.appendChild(xml.createElement('tag'))
            tag_elem.appendChild(xml.createTextNode(tag))

        tagmap_elem = config_elem.appendChild(xml.createElement('tagmap'))
        for from_tag, to_tag in self.tagmap:
            mapping_elem = tagmap_elem.appendChild(xml.createElement('mapping'))
            from_elem = mapping_elem.appendChild(xml.createElement('from'))
            from_elem.appendChild(xml.createTextNode(from_tag))
            to_elem = mapping_elem.appendChild(xml.createElement('to'))
            to_elem.appendChild(xml.createTextNode(to_tag))

        xml.writexml(file, '', '  ', "\n", 'UTF-8')

    def _parse_settings(self, settings):
        for node in settings.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                self.set(node.tagName, node.firstChild.nodeValue)
    
    def _parse_tags(self, tags):
        for node in tags.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                self.add_tag(node.firstChild.nodeValue.strip())
    
    def _parse_tagmap(self, tagmap):
        for node in tagmap.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                from_val = node.getElementsByTagName('from').item(0).firstChild.nodeValue.strip()
                to_val = node.getElementsByTagName('to').item(0).firstChild.nodeValue.strip()
                self.add_mapping(from_val, to_val)
