from protocol_element import ProtocolElement

class ProtocolPacket(ProtocolElement):
    def __init__(self, file_name, xml, settings, **kwargs):
        ProtocolElement.__init__(self, 'packet', file_name, xml, settings,
                                required_keys=
                                [
                                    'name'
                                ])
        
    
    def parse(self, xml):
        attr = xml.attrib
        self.name = attr.get('name')
        self.id = attr.get('id', self.name)
        
        
    def full_name(self):
        return self.settings.prefix + self.name + self.settings.packet_suffix