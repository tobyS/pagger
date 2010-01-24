# -*- coding: utf-8 -*-
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

    ignore = set()

    tagmap = {}

    _changed = False

    _file = None

    def __init__(self, file):
        self._file = file
        self.load_file(file)

    def load_file(self, file):
        dom = parse(file)
        self._parse_settings(dom.getElementsByTagName('settings').item(0))
        self.tags = self._parse_set(dom.getElementsByTagName('tags').item(0), 'tag', unicode)
        for tag in self.tags:
            self.tagmap[tag.lower()] = tag
        self.ignore = self._parse_set(dom.getElementsByTagName('ignore').item(0), 'match', unicode)
        self._parse_tagmap(dom.getElementsByTagName('tagmap').item(0))
        self._changed = False

    def add_tag(self, tag):
        self.tags.add(tag)
        self.tagmap[tag.lower()] = tag
        self._changed = True

    def add_mapping(self, from_tag, to_tag):
        self.tagmap[from_tag.lower()] = to_tag
        self._changed = True

    def set(self, key, val):
        if key not in self._available_settings:
            raise RuntimeError('Invalid setting "' + key + '".')
        self.settings[key] = self._available_settings[key](val)
        self._changed = True

    def save(self):
        impl = getDOMImplementation()
        xml = impl.createDocument(None, 'config', None)
        config_elem = xml.documentElement

        settings_elem = config_elem.appendChild(xml.createElement('settings'))
        self._save_settings(xml, settings_elem)

        tags_elem = config_elem.appendChild(xml.createElement('tags'))
        self._save_set(xml, tags_elem, 'tag', self.tags)

        ignore_elem = config_elem.appendChild(xml.createElement('ignore'))
        self._save_set(xml, ignore_elem, 'match', self.ignore)

        tagmap_elem = config_elem.appendChild(xml.createElement('tagmap'))
        self._save_mappings(xml, tagmap_elem, self.tagmap)

        xml.writexml(open(self._file, 'w'), '', '  ', "\n", 'UTF-8')
        self._changed = False

    def changed(self):
        return self._changed

    def _save_settings(self, xml, parent):
        for key, val in self.settings.items():
            setting_elem = parent.appendChild(xml.createElement(key))
            setting_elem.appendChild(xml.createTextNode(str(val)))

    def _save_mappings(self, xml, parent, dict):
        for key, val in dict.items():
            if key == val.lower():
                continue
            mapping_elem = parent.appendChild(xml.createElement('mapping'))
            from_elem = mapping_elem.appendChild(xml.createElement('from'))
            from_elem.appendChild(xml.createTextNode(key))
            to_elem = mapping_elem.appendChild(xml.createElement('to'))
            to_elem.appendChild(xml.createTextNode(val))


    def _save_set(self, xml, parent, tag_name, set):
        for item in set:
            elem = parent.appendChild(xml.createElement(tag_name))
            elem.appendChild(xml.createTextNode(str(item)))

    def _parse_settings(self, settings):
        for node in settings.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                self.set(node.tagName, node.firstChild.nodeValue)
    
    def _parse_tags(self, tags):
        for node in tags.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                self.add_tag(node.firstChild.nodeValue.strip())

    def _parse_set(self, root, elem_tag, type):
        elements = set()
        for node in root.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.tagName == elem_tag:
                elements.add(type(node.firstChild.nodeValue.strip()))

        return elements
    
    def _parse_tagmap(self, tagmap):
        for node in tagmap.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                from_val = node.getElementsByTagName('from').item(0).firstChild.nodeValue.strip()
                to_val = node.getElementsByTagName('to').item(0).firstChild.nodeValue.strip()
                self.add_mapping(from_val, to_val)
