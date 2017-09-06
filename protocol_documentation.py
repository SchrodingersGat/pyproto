from protocol_element import ProtocolElement

class ProtocolDocumentation(ProtocolElement):
    def __init__(self, file_name, xml, settings, **kwargs):
        ProtocolElement.__init__(self, 'doc', file_name, xml, settings,
                                required_keys=
                                [
                                    'comment'
                                ])
    
        
    def parse(self, xml):
        pass