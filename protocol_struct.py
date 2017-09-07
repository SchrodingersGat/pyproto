from collections import OrderedDict

from protocol_element import ProtocolElement
from protocol_variable import ProtocolVariable

class ProtocolStruct(ProtocolElement):
    def __init__(self, protocol, file_name, xml, **kwargs):
        ProtocolElement.__init__(self, protocol, 'struct', file_name, xml,
                                required_keys=
                                [
                                    'name'
                                ])
    
    
    def parse(self, xml):
    
        self.data = OrderedDict()
        
        for node in xml:
        
            # Structs can be defined in other structs!
            if node.tag.lower() in ['struct', 'structure']:
                struct = ProtocolStruct(self.protocol, self.file_name, node)
                self.protocol.add_element(struct)
                
                self.add_data(struct, struct.name)
                
        
            elif node.tag.lower() == 'data':
            
                ref_name = node.attrib.get('name', None)
                if not ref_name:
                    self.warning("Struct {s} contains data element missing 'name' field".format(s=self.full_name))
                    continue
            
                # Is the data element a struct?
                struct_name = node.attrib.get('struct', None)
                
                if struct_name:
                    # Attempt to find the referenced struct
                    struct_ref = self.protocol.get_struct_by_name(struct_name)
                    
                    if not struct_ref:
                        self.error("Could not locate struct '{s}' in {me}".format(s=struct_name, me=str(self)))
                    
                    self.add_data(struct_ref, ref_name)
                    
                else:
                    var = ProtocolVariable(self.protocol, self.file_name, node)
                    self.add_data(var, ref_name)
            else:
                print("Found unknown tag '{t}' parsing struct '{n}'".format(t=node.tag, n=self.full_name))
                
            
    def add_data(self, data_object, ref_name):
    
        t = type(data_object)
    
        for d in self.data:
            if d == ref_name:
                self.warning("Struct {s} contains multiple references to '{n}'".format(s=self.full_name, n=ref_name))
                return False
 
        self.data[ref_name] = data_object
        
        
    @property
    def variables(self):
        v = OrderedDict()        
        for key, value in self.data.items():
            if type(value) == ProtocolVariable:
                v[key] = value
                
        return v
        
    @property
    def structs(self):
        s = OrderedDict()
        for key, value in self.data.items():
            if type(value) == ProtocolStruct:
                s[key] = value
        
        return s
            
            
    @property
    def suffix(self):
        return self.protocol.struct_suffix