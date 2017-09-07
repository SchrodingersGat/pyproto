from protocol_element import ProtocolElement

class ProtocolPacket(ProtocolElement):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'packet', file_name, xml,
                                required_keys=
                                [
                                    'name'
                                ])
        
    
    def parse(self, xml):
        pass
        
        
    @property
    def suffix(self):
        return self.settings.packet_suffix