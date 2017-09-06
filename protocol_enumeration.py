from protocol_element import ProtocolElement

class ProtocolEnumeration(ProtocolElement):
    def __init__(self, file_name, xml, settings, **kwargs):
        ProtocolElement.__init__(self, 'enum', file_name, xml, settings,
                                required_keys=[
                                    'name',
                                ])
        
    
    def parse(self, xml):
        attrib = xml.attrib
        self.name = attrib['name']
        
        # Iterate over data tags
        for data in xml.findall('data'):
            print("Data:", data)
            
        
    def full_name(self):
        #TODO - Improve
        return self.settings.prefix + self.name