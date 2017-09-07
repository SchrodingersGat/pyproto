class ProtocolElement:

    TRUE_VALUES = ['y', 'yes', '1', 'true', 'on']
    FALSE_VALUES = ['n', 'no', '0', 'false', 'off']
    
    
    def __init__(self, protocol, element_type, file_name, xml, required_keys=[]):
        self.element_type = element_type
        self.xml = xml
        
        # Extract all attributes and convert keys to lower case
        # (this simplifies case matching later on)
        self.attrib = {}
        for k in self.xml.attrib:
            self.attrib[k.lower()] = self.xml.attrib[k]
        
        self.file_name = file_name
        
        self.require_keys(required_keys)
        
        self.protocol = protocol
        
        # Add debug hooks for easy use
        self.debug = protocol.debug
        self.critical = protocol.critical
        self.error = protocol.error
        self.warning = protocol.warning
        self.info = protocol.info
        self.extra = protocol.extra
        
        self.debug(self.protocol.DEBUG_LVL_INFO, "Parsing {e} <{n}>".format(e=self.element_type, n=self.pretty_name))
        
        self.parse(xml)
        
        
    def parse(self, xml):
        # Default implementation does nothing
        pass
        
        
    def get_value(self, name):
        return self.attrib.get(name.lower(), '')
        
        
    def is_value_set(self, name):  
        return self.get_value(name).lower() in self.TRUE_VALUES
    
        
    def __getattr__(self, name):
        # By default, search the xml tag, returning a blank string if not found
        return self.get_value(name)
        
    
    @property
    def full_name(self):
        # Default implementation just returns the best guess for name
        # Override in subclass as appropriate
        return self.prefix + self.name + self.suffix
        
        
    @property
    def pretty_name(self):
        return self.full_name
        
        
    @property
    def id(self):
        # Default implementation searches for ID, and if not found, uses name
        # Override in subclass as appropriate
        return self.attrib.get('id', self.name)
        
        
    def require_keys(self, keys):    
        for k in keys:
        
            # Simple string keys
            if type(k) is str and not k in self.xml.attrib:
                error_msg = "{e} is missing key '{k}'\n".format(e=self.element_type, k=k)
                error_msg += "in file {f}\n".format(f=self.file_name)
                error_msg += "{d}".format(d=self.xml.attrib)
                
                self.error(error_msg)
                
            # List of optional keys, at least one must be set
            elif type(k) in [list, tuple] and not any([kk in self.xml.attrib for kk in k]):
                self.error("no keys in {k} found".format(k=k))
                
                
    def __repr__(self):
        return "{t}<{n}>".format(t=self.element_type, n=self.pretty_name)