from __future__ import print_function

import os

# xml parser module
from xml.etree import ElementTree

from protocol_tag import ProtocolTag
from protocol_struct import ProtocolStruct
from protocol_enumeration import ProtocolEnumeration
from protocol_documentation import ProtocolDocumentation
from protocol_packet import ProtocolPacket
from protocol_settings import ProtocolSettings

DEBUG_CRITICAL = 0
DEBUG_ERROR = 1
DEBUG_WARNING = 2
DEBUG_INFO = 3
DEBUG_EXTRA = 4

# Simple debug handler
DEBUG_LEVEL = DEBUG_EXTRA

def debug(level, *arg):
    if level <= DEBUG_LEVEL:
        print(" ".join([a for a in arg]))
        

class ProtocolParser:
    """ Class ProtocolParser
    Reads one (or more) xml protocol description files
    """
    
    def __init__(self, root_file, **kwargs):
        
        self.settings = ProtocolSettings()
        
        # Extract the absolute path of the root file
        root_path = os.path.abspath(root_file)
        
        self.elements = []
        self.structures = []
        self.enumerations = []
        self.packets = []
        self.docs = []
        self.files = []
        self.unknown = []
        
        if not self.parse_file(root_path):
            debug(DEBUG_CRITICAL, "Could not parse protocol file")
    
    def parse_file(self, file_name, **kwargs):
    
        dir_name = kwargs.get('dir_name', None)
        optional = kwargs.get('optional', False)
    
        if dir_name is not None:
            file_name = os.path.join(dir_name, file_name)
            
        file_name = os.path.abspath(file_name)
        base_dir = os.path.dirname(file_name)
        
        if not os.path.exists(file_name):
            if optional:
                debug(DEBUG_WARNING, "Optional file '{f}' not found".format(f=file_name))
                return False
            else:
                raise NameError("File '{f}' does not exist".format(f=file_name))
        
        debug(DEBUG_INFO, "Parsing '{f}'".format(f=file_name))
        
        if file_name in self.files:
            debug(DEBUG_WARNING, "Skipping file '{f}' as it has already been parsed".format(f=file_name))
            return False
        
        self.files.append(file_name)
        
        # Open the file and extract xml data
        with open(file_name, 'r') as xml_file:
            xml = ElementTree.parse(xml_file)
        
        # Find the root tag
        root = xml.getroot()
        
        if not ProtocolTag.compare(root.tag, ProtocolTag.PROTOCOL):
            debug(DEBUG_CRITICAL, "Expected 'protocol' tag, found '{t}' instead".format(t=root.tag))
            return
        
        # Root file is supplied without a directory name
        # Extract protocol information at this stage
        if dir_name is None:
            self.settings.set_parameters(root.attrib)
        
        # Iterate through each top-level child tags
        for node in root:
            tag = node.tag
            
            # Include a subsequent file?
            if ProtocolTag.compare(tag, ProtocolTag.REQUIRE):
                required_file = node.attrib.get('file', None)
                optional = node.attrib.get('optional', False)
                
                if required_file is not None:
                
                    # Option to include all .xml files in a directory
                    if required_file.endswith('*'):
                        required_file = os.path.join(base_dir, required_file)
                        required_dir = os.path.dirname(required_file)
                        if os.path.exists(required_dir) and os.path.isdir(required_dir):
                            dir_files = os.listdir(required_dir)
                            
                            for f in dir_files:
                            
                                if f.endswith('.xml'):
                                    self.parse_file(f, dir_name=required_dir, optional=True)
                        else:
                            debug(DEBUG_WARNING, "Could not find required directory '{d}'".format(d=required_dir))
                
                    else:
                        self.parse_file(required_file, dir_name=base_dir, optional=optional)
                    
            # Structure?
            elif ProtocolTag.compare(tag, ProtocolTag.STRUCTURE):
                struct = ProtocolStruct(file_name, node, self.settings)
                
                self.add_struct(struct)

            # Enumeration?
            elif ProtocolTag.compare(tag, ProtocolTag.ENUM):
                enum = ProtocolEnumeration(file_name, node, self.settings)
                self.add_enumeration(enum)
                
            # Documentation?
            elif ProtocolTag.compare(tag, ProtocolTag.DOC):
                doc = ProtocolDocumentation(file_name, node, self.settings)
                self.add_documentation(doc)
                
            # Packet?
            elif ProtocolTag.compare(tag, ProtocolTag.PACKET):
                pkt = ProtocolPacket(file_name, node, self.settings)
                self.add_packet(pkt)
                    
            else:
                # Unknown tag
                #TODO
                pass
                
        # File parsing was successful
        return True
        
    
    def add_struct(self, struct): 
        for s in self.structures:
            if s.full_name == struct.full_name:
                debug(DEBUG_WARNING, "Found duplicate struct named '{name}' : ignoring".format(name=struct.full_name()))
                
        self.structures.append(struct)
        self.elements.append(struct)
           
           
    def add_enumeration(self, enum):
        for e in self.enumerations:
            if e.full_name == enum.full_name:
                debug(DEBUG_WARNING, "Found duplicate enum named '{name}' : ignoring".format(name=enum.full_name()))
                
        self.enumerations.append(enum)
        self.elements.append(enum)
        
        
    def add_documentation(self, doc):
        self.docs.append(doc)
        self.elements.append(doc)
        
        
    def add_packet(self, pkt):
        for p in self.packets:
            if p.full_name() == pkt.full_name:
                debug(DEBUG_WARNING, "Found duplicate packet named '{name}' : ignoring".format(name=pkt.full_name()))
                
        self.packets.append(pkt)
        self.elements.append(pkt)
        
 
if __name__ == "__main__":
    f = "test_protocol.xml"
    
    parser = ProtocolParser(f)
    
    print(parser.elements)