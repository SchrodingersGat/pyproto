from __future__ import print_function

import sys, os

from protocol import Protocol
        

class ProtocolParser:
    """ Class ProtocolParser
    Reads one (or more) xml protocol description files
    """
    
    def __init__(self, root_file, **kwargs):
    
        self.protocol = Protocol()
        
        self.protocol.set_debug_level(Protocol.DEBUG_LVL_WARNING)
        
        self.debug = self.protocol.debug
        
        # Extract the absolute path of the root file
        root_path = os.path.abspath(root_file)
        
        if not self.protocol.parse_file(root_path):
            self.debug(Protocol.DEBUG_LVL_CRITICAL, "Could not parse protocol file")
        
 
if __name__ == "__main__":
    f = "test_protocol.xml"
    
    parser = ProtocolParser(f)
    
    print(parser.protocol.elements)