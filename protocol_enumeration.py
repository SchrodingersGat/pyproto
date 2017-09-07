from protocol_element import ProtocolElement

class ProtocolEnumeration(ProtocolElement):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'enum', file_name, xml,
                                required_keys=[
                                    'name',
                                ])
        
    
    def parse(self, xml):
        attrib = xml.attrib
        
        # Iterate over data tags
        for data in xml.findall('data'):
            print("Data:", data)