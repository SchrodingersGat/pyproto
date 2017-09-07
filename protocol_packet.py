from protocol_struct import ProtocolStruct
from protocol_element import ProtocolElement

class ProtocolPacket(ProtocolStruct):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'packet', file_name, xml,
                                required_keys=
                                [
                                    'name'
                                ])
        
        
    @property
    def suffix(self):
        return self.protocol.packet_suffix