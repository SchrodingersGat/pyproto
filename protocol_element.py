class ProtocolElement:

    def __init__(self, element_type, file_name, xml, settings, required_keys=[]):
        self.element_type = element_type
        self.xml = xml
        
        # Extract all attributes and convert keys to lower case
        # (this simplifies case matching later on)
        self.attrib = {}
        for k in self.xml.attrib:
            self.attrib[k.lower()] = self.xml.attrib[k]
        
        self.file_name = file_name
        self.settings = settings
        
        self.require_keys(required_keys)
        
        print("parsing element:", self.element_type)
        
        self.parse(xml)
        
        
    def parse(self):
        # Default implementation does nothing
        pass
        
    def __getattr__(self, name):
        name = name.lower()
        # By default, search the xml tag, returning a blank string if not found
        return self.attrib.get(name, '')

    
    @property
    def full_name(self):
        # Default implementation just returns the best guess for name
        # Override in subclass as appropriate
        return self.prefix + self.name + self.suffix
        
        
    @property
    def prefix(self):
        return self.settings.prefix
        
        
    @property
    def suffix(self):
        return ''
        
        
    @property
    def id(self):
        # Default implementation searches for ID, and if not found, uses name
        # Override in subclass as appropriate
        return self.attrib.get('id', self.name)
        
        
    def require_keys(self, keys):    
        for k in keys:
        
            # Simple string keys
            if type(k) is str and not k in self.xml.attrib:
                error_msg = "{e} is missing key '{k}' ".format(e=self.element_type, k=k)
                error_msg += "in file {f}".format(f=self.file_name)
                error_msg += " : {d}".format(d=self.xml.attrib)
                
                raise KeyError(error_msg)
                
            # List of optional keys, at least one must be set
            elif type(k) in [list, tuple] and not any([kk in self.xml.attrib for kk in k]):
                raise KeyError("no keys in {k} found".format(k=k))
                
                
    def __repr__(self):
        return "{t}<{n}>".format(t=self.element_type, n=self.full_name)