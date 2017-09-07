from __future__ import print_function

from protocol_struct import ProtocolStruct
from protocol_enumeration import ProtocolEnumeration
from protocol_packet import ProtocolPacket
from protocol_documentation import ProtocolDocumentation

import sys
import os
from xml.etree import ElementTree

class Protocol:

    DEBUG_LVL_CRITICAL = 0
    DEBUG_LVL_ERROR = 1
    DEBUG_LVL_WARNING = 2
    DEBUG_LVL_INFO = 3
    DEBUG_LVL_EXTRA = 4
    
    DEBUG_LVL_OFF = -1

    def __init__(self, params={}, **kwargs):
        self.set_parameters(params)
    
        self.elements = []
        self.structs = []
        self.enums = []
        self.packets = []
        self.docs = []
        self.unknown = []
        
        self.files = []
        
        self.set_debug_level(kwargs.get('debug_level', self.DEBUG_LVL_WARNING))
        
    def set_debug_level(self, level):
        self.debug_level = level
        
        
    def debug(self, level, *arg):
        
        debug_text = ["CRITICAL", "ERROR", "WARNING", "INFO", "EXTRA"]
        
        if level >= 0 and level < len(debug_text):
            lvl = debug_text[level]
        else:
            lvl = "DEBUG"
    
        if level <= self.debug_level:
            print(lvl + " : " + " ".join([a for a in arg]))
            
        if level <= self.DEBUG_LVL_ERROR:
            sys.exit(1)
        
    
    def extra(self, *arg):
        self.debug(self.DEBUG_LVL_EXTRA, *arg)
        
        
    def info(self, *arg):
        self.debug(self.DEBUG_LVL_INFO, *arg)
        
        
    def warning(self, *arg):
        self.debug(self.DEBUG_LVL_WARNING, *arg)
        
        
    def error(self, *arg):
        self.debug(self.DEBUG_LVL_ERROR, *arg)
        
        
    def critical(self, *arg):
        self.debug(self.DEBUG_LVL_CRITICAL, *arg)
        
        
    def parse_file(self, file_name, **kwargs):
        dir_name = kwargs.get('dir_name', None)
        optional = kwargs.get('optional', False)
    
        if dir_name is not None:
            file_name = os.path.join(dir_name, file_name)
            
        file_name = os.path.abspath(file_name)
        base_dir = os.path.dirname(file_name)
        
        if not os.path.exists(file_name):
            if optional:
                self.warning("Optional file '{f}' not found".format(f=file_name))
                return False
            else:
                self.error("File '{f}' does not exist".format(f=file_name))
        
        self.info("Parsing '{f}'".format(f=file_name))
        
        if file_name in self.files:
            self.warning("Skipping file '{f}' as it has already been parsed".format(f=file_name))
            return False
        
        self.files.append(file_name)
        
        # Open the file and extract xml data
        with open(file_name, 'r') as xml_file:
            xml = ElementTree.parse(xml_file)
        
        # Find the root tag
        root = xml.getroot()
        
        if not root.tag.lower() == 'protocol':
            self.critical("Expected 'protocol' tag, found '{t}' instead".format(t=root.tag))
            return
        
        # Root file is supplied without a directory name
        # Extract protocol information at this stage
        if dir_name is None:
            self.set_parameters(root.attrib)
        
        # Iterate through each top-level child tags
        for node in root:
            tag = node.tag
            
            # Include a subsequent file?
            if tag.lower() in ['require']:
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
                            self.warning("Could not find required directory '{d}'".format(d=required_dir))
                
                    else:
                        self.parse_file(required_file, dir_name=base_dir, optional=optional)
                    
            # Structure?
            elif tag.lower() in ['struct', 'structure']:
                struct = ProtocolStruct(self, file_name, node)
                
                self.add_element(struct)

            # Enumeration?
            elif tag.lower() in ['enum', 'enumeration']:
                enum = ProtocolEnumeration(self, file_name, node)
                self.add_element(enum)
                
            # Documentation?
            elif tag.lower() in ['doc', 'documentation']:
                doc = ProtocolDocumentation(self, file_name, node)
                self.add_element(doc)
                
            # Packet?
            elif tag.lower() in ['pkt', 'packet']:
                pkt = ProtocolPacket(self, file_name, node)
                self.add_element(pkt)
                    
            else:
                self.add_element(node)
                
        # File parsing was successful
        return True
        
    
    def set_parameters(self, params):
        self.prefix = params.get('prefix', '')
        self.endian = params.get('endian', 'big').lower()
        
        if not self.endian in ['big', 'little']:
            raise ValueError("Protocol endianness should be either 'big' or 'little' (found '{e}')".format(e=self.endian))
        
        self.packet_suffix = params.get('packetSuffix', '_Packet_t')
        self.struct_suffix = params.get('structSuffix', '_t')
        
        self.version = params.get('version', '0.0')
        
        self.comment = params.get('comment', '')
        
        # Default packet pointer
        self.pointer = params.get('pointer', 'void*')
        
        
    def add_element(self, element):
        
        t = type(element)
        
        if t == ProtocolPacket:
            # Ensure that a duplicate packet is not found
            for pkt in self.packets:
                if pkt.full_name == element.full_name:
                    self.warning("Found duplicate packet '{n}', skipping".format(n=pkt.full_name))
                    return False
                    
            self.packets.append(element)
                
        elif t == ProtocolStruct:
            for struct in self.structs:
                if struct.full_name == element.full_name:
                    self.warning("Found duplicate struct '{n}', skipping".format(n=struct.full_name))
                    return False
                    
            self.structs.append(element)
    
        elif t == ProtocolEnumeration:
            for enum in self.enums:
                if enum.full_name == element.full_name:
                    self.warning("Found duplicate enum '{n}', skipping".format(n=enum.full_name))
                    return False
                    
            self.enums.append(element)
            
        elif t == ProtocolDocumentation:
            self.docs.append(element)
    
        else:
            self.info("add_element called with unknown element : {e}".format(e=element))
            self.unknown.append(element)
            return False
                
                
        self.elements.append(element)
        return True
        
        
    def get_struct_by_name(self, name):
        
        self.extra("Looking for struct '{n}'".format(n=name))
        
        s = None
        
        # Search first by full name
        for struct in self.structs:
            if struct.full_name == name:
                s = struct
                break
                
        if not s:
            # Search next by short name
            for struct in self.structs:
                if struct.name == name:
                    s = struct
                    break
                
        if not s:
            # Search next by adding prefix and suffix
            long_name = self.prefix + name + self.struct_suffix
            
            for struct in self.structs:
                if struct.name == long_name:
                    s = struct
                    break
                
        if not s:
            # Could not find struct with given name
            self.warning("Could not find referenced struct '{s}'".format(s=name))
            return None
            
        self.extra("Found corresponding struct '{n}'".format(n=s.full_name))
        return s