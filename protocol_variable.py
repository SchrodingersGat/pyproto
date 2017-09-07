import re

from protocol_element import ProtocolElement

class ProtocolVariable(ProtocolElement):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'variable', file_name, xml,
                                required_keys=
                                [
                                ])
                                
    
    def parse(self, xml):        
        if not self.memory_type:
            self.warning("Variable '{v}' does not define inMemoryType".format(v=self.full_name))
    
    
    @property
    def pretty_name(self):
        return '{v} ({t})'.format(v=self.name, t=self.std_type(self.memory_type))
    
    
    @property
    def memory_type(self):
        return self.inMemoryType
    
    
    @property
    def encoded_type(self):
        return self.attrib.get('encodedtype', self.memory_type)
    
    
    def std_type(self, type_name):
        # Convert a type-name to a C std type
        
        type_name = type_name.lower()
        
        # Allowed raw strings
        if type_name in ['float', 'double', 'null', 'none']:
            return type_name
        
        # First attempt to convert from unsigned<x> to uint<x>_t
        r = '(un)?signed(\d+)'
        
        result = re.search(r, type_name)
            
        if result is not None and len(result.groups()) == 2:
            g = result.groups()
            d = int(g[1])
            
            if not d in [8, 16, 24, 32, 48, 64]:
                self.warning('Variable {n} has improper datatype: {t}'.format(n=self.name, t=type_name))
            
            tn = '{u}int{n}_t'.format(u='u' if g[0] is not None else '', n=g[1])
            return tn
            
        # Look for format (u)int<x>(_t)
        r = '(u)?int(\d+)(_t)?'
        
        result = re.search(r, type_name)
        
        if result is not None and len(result.groups()) == 3:
            g = result.groups()
            d = int(g[1])
            
            if not d in [8, 16, 24, 32, 48, 64]:
                self.warning('Variable {n} has improper datatype: {t}'.format(n=self.name, t=type_name))
            tn = '{u}int{d}_t'.format(u = 'u' if g[0] is not None else '', d = g[1])
            return tn
            
        # Could not convert to a standard type!
        self.warning("Could not convert '{t}' to a standard type for variable '{v}'".format(t=type_name, v=self.name))
        return type_name
        
        
    def is_float(self):
        return self.memory_type in ['float', 'double']
        
        
    def is_integer(self):
        return 'int' in std.std_type(self.memory_type)
        
        
    def is_signed(self):
        return self.is_integer() and not self.std_type(self.memory_type).starts_with('u')
        
        
    def is_null(self):
        return self.memory_type.lower() in ['null', 'none']
        
        
    @property
    def prefix(self):
        return ''