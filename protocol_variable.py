from protocol_element import ProtocolElement

class ProtocolVariable(ProtocolElement):
    def __init__(self, file_name, xml, settings, **kwargs):
        ProtocolElement.__init__(self, 'variable', file_name, xml, settings,
                                required_keys=
                                [
                                ])