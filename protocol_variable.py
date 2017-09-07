import re

from protocol_element import ProtocolElement

class ProtocolVariable(ProtocolElement):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'variable', file_name, xml,
                                required_keys=
                                [
                                ])
                                
    
    def parse(self, xml):        
        if not self.get_memory_type():
            self.warning("Variable '{v}' does not define inMemoryType".format(v=self.full_name))
    
    
    @property
    def pretty_name(self):
        return '{v} ({t}{a})'.format(v=self.name,
                                  t=self.std_type(self.get_memory_type()),
                                  a=' [{a}]'.format(a=self.array_size) if self.is_array() else '')
        
    
    
    def get_memory_type(self, std=True):
        """ 
        Return the in-memory type for this variable
        """
        
        t = self.inMemoryType
        if std:
            t = self.std_type(t)
        return t
    
    
    def get_encode_type(self, std=True):
        """
        Return the encoded type for this variable
        If 'encodedType' is not explicitly provided, then inMemoryType is used
        """
        
        t = self.attrib.get('encodedtype', self.get_memory_type(std))
        if std:
            t = self.std_type(t)
        return t
        
        
    def is_array(self):
        return self.array_size > 1
            
            
    @property
    def array_size(self):
        """ 
        Extract the array size for this variable
        """
        
        if not self.array:
            return 0
            
        try:
            n = int(self.array)
            if n < 0:
                n = 0
            return n
        except:
            return 0
    
    
    def std_type(self, type_name):
        """
        Convert a type-name to a C std type
        """
        
        type_name = type_name.lower()
        
        # Allowed raw strings
        if type_name in ['float', 'double', 'null', 'none']:
            return type_name
        
        # First attempt to convert from unsigned<x> to uint<x>_t
        r = '(un)?signed(\d+)'
        
        result = re.search(r, type_name)
            
        if result and len(result.groups()) == 2:
            g = result.groups()
            d = int(g[1])
            return self.format_integer_type(d, not g[0]=='un')
            
        # Look for format (u)int<x>(_t)
        r = '(u)?int(\d+)(_t)?'
        
        result = re.search(r, type_name)
        
        if result and len(result.groups()) == 3:
            g = result.groups()
            d = int(g[1])
            return self.format_integer_type(d, not g[0]=='u')
            
        # Look for format [ui]<d>
        r = '([ui])(\d+)(_t)?'
        
        result = re.search(r, type_name)
        
        if result and len(result.groups()) == 3:
            g = result.groups()
            d = int(g[1])
            return self.format_integer_type(d, g[0] == 'i')
            
        # Could not convert to a standard type!
        self.warning("Could not convert '{t}' to a standard type for variable '{v}'".format(t=type_name, v=self.name))
        return type_name
        
        
    def format_integer_type(self, n, signed=False):
        if not n in [8, 16, 24, 32, 48, 64]:
            self.warning("Integer cannot be of base '{n}'".format(n=n))
        return "{u}int{d}_t".format(u='u' if not signed else '', d=n)
        
        
    def is_float(self):
        """
        Returns true if this variable is a floating point number
        """
        return self.memory_type in ['float', 'double']
        
        
    def is_integer(self):
        """
        Returns true if this variable is an integer
        """
        return 'int' in std.std_type(self.memory_type)
        
        
    def is_signed(self):
        """
        Returns true if this variable is a signed integer
        """
        return self.is_integer() and not self.std_type(self.memory_type).starts_with('u')
        
        
    def is_null(self):
        """
        Returns true if the in-memory type for this variable is null
        (This means that the variable will not be stored in memory
        """
        return self.memory_type.lower() in ['null', 'none']
        
        
    def has_initializers(self):
        """
        Returns true if this variable defines default min/max values
        """
        return self.defaultMinValue or self.defaultMaxValue
        
        
    def has_validators(self):
        """
        Returns true if this variable defines min/max values for validation
        """
        return self.verifyMinValue or self.verifyMaxValue
        
        
    @property
    def prefix(self):
        return ''