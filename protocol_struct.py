from protocol_element import ProtocolElement
from protocol_variable import ProtocolVariable

class ProtocolStruct(ProtocolElement):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'struct', file_name, xml,
                                required_keys=
                                [
                                    'name'
                                ])
    
    
    def parse(self, xml):
        attrib = xml.attrib
        
        for node in xml:
            if node.tag.lower() == 'data':
                struct_name = node.attrib.get('struct', None)
                print(node)
            else:
                print("Found unknown tag '{t}' parsing struct '{n}'".format(t=node.tag, n=self.full_name))
            
            
    @property
    def suffix(self):
        return self.settings.struct_suffix