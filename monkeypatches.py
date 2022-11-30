from defusedxml.minidom import parseString
from json2xml import json2xml
from json2xml import dicttoxml
from pyexpat import ExpatError
from json2xml.utils import InvalidDataError

def mp_to_xml(self):
    """
    Convert to xml using dicttoxml.dicttoxml and then pretty print it.
    """
    if self.data:
        xml_data = dicttoxml.dicttoxml(
            self.data,
            root=self.root,
            custom_root=self.wrapper,
            attr_type=self.attr_type,
            item_wrap=self.item_wrap,
        )
        if self.pretty:
            try:
                result = parseString(xml_data).toprettyxml(encoding='utf-8', standalone=True)
            except ExpatError:
                raise InvalidDataError
            return result
        return xml_data
    return None

json2xml.Json2xml.to_xml = mp_to_xml