from xml.dom.minidom import parseString

from lastfm.tag import Tag

class TagParser:

    def parse_tags(self, xml):
        try:
            dom = parseString(xml)
        except xml.parsers.expat.ExpatError:
            print u'Could not parse XML response "' + xml + '"'
            return []
        tags = []
        for tag_element in dom.getElementsByTagName('tag'):
            tags.append(self._parse_tag(tag_element))
        return tags

    def _parse_tag(self, tag_element):
        return Tag(
                tag_element.getElementsByTagName('name').item(0).firstChild.nodeValue,
                tag_element.getElementsByTagName('url').item(0).firstChild.nodeValue,
                int(tag_element.getElementsByTagName('count').item(0).firstChild.nodeValue)
                    if tag_element.getElementsByTagName('count').length > 0
                    else -1
        )

