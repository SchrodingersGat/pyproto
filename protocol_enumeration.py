from protocol_element import ProtocolElement


class ProtocolEnumerationValue(ProtocolElement):
    def __init__(self, protocol, parent_enum, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'enumvalue', file_name, xml,
                                required_keys=[
                                    'name',
                                ])
                               
        # Reference to the enumeration of which this value is a child
        self.enum = parent_enum
                                
            
    @property
    def full_name(self):
        pre = "" if self.is_value_set('ignorePrefix') else self.enum.valuePrefix
        suf = "" if self.is_value_set('ignoreSuffix') else self.enum.valueSuffix
        
        return pre + self.name + suf


class ProtocolEnumeration(ProtocolElement):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'enum', file_name, xml,
                                required_keys=[
                                    'name',
                                ])
        
    
    def parse(self, xml):
    
        self.values = []
        
        for node in xml:
            if node.tag.lower() in ['val', 'value']:
                self.add_value(ProtocolEnumerationValue(self.protocol, self, self.file_name, node))
                
    
    def add_value(self, value):
        self.values.append(value)