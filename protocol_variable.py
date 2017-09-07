from protocol_element import ProtocolElement

class ProtocolVariable(ProtocolElement):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'variable', file_name, xml,
                                required_keys=
                                [
                                ])
                                
    
    def parse(self, xml):
        print("Parsing variable '{v}'".format(v=self.full_name))