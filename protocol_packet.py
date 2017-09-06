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
        
        
    @property
    def suffix(self):
        return self.settings.packet_suffix