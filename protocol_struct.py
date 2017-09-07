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
    
        self.child_items = OrderedDict()
        
        for node in xml:
        
            # Structs can be defined in other structs!
            if node.tag.lower() in ['struct', 'structure']:
                struct = ProtocolStruct(self.protocol, self.file_name, node)
                self.protocol.add_element(struct)
                
                self.add_child(struct, struct.name)
                
        
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
                    
                    self.add_child(struct_ref, ref_name)
                    
                else:
                    var = ProtocolVariable(self.protocol, self.file_name, node)
                    self.add_child(var, ref_name)
            else:
                print("Found unknown tag '{t}' parsing struct '{n}'".format(t=node.tag, n=self.full_name))
                
            
    def add_child(self, data_object, ref_name):
    
        t = type(data_object)
    
        for d in self.child_items:
            if d == ref_name:
                self.warning("Struct {s} contains multiple references to '{n}'".format(s=self.full_name, n=ref_name))
                return False
 
        self.child_items[ref_name] = data_object
        
        
    def children(self, filter_list=None):
        childs = OrderedDict()
        
        for key, value in self.child_items.items():
            if filter_list is None or type(value) in filter_list:
                childs[key] = value
                
        return childs
        
        
    @property
    def variables(self):
        return self.children([ProtocolVariable])
        
    @property
    def structs(self):
        return self.children([ProtocolStruct])    
            
    @property
    def suffix(self):
        return self.protocol.struct_suffix
        
        
    def has_validators(self):
        """
        Return true if this struct has any validators. 
        This is true if any of the following conditions are met:
        a) Any variables in this struct have validators
        b) Any child structs satisfy the 'has_validators' check
        """
        childs = self.children([ProtocolStruct, ProtocolVariable])

        for child_name, child in childs.items():
            if child.has_validators():
                return True
                
        return False
        
        
    def has_initializers(self):
        """
        Return true if this struct has any initializers.
        This is true if any of the following conditions are met:
        a) Any variables in this struct have initializers
        b) Any child structs satisfy the 'has_initializers' check
        """
        childs = self.children([ProtocolStruct, ProtocolVariable])
        
        for child_name, child in childs.items():
            if child.has_initializers():
                return True
                
        return False
    