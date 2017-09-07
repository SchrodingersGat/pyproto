from protocol_element import ProtocolElement

class ProtocolDocumentation(ProtocolElement):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'doc', file_name, xml,
                                required_keys=
                                [
                                    'comment'
                                ])
    
        
    def parse(self, xml):
        pass