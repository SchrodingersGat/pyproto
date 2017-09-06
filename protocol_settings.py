class ProtocolSettings:
    def __init__(self, params={}):
        self.set_parameters(params)
    
    
    def set_parameters(self, params):
        self.prefix = params.get('prefix', '')
        self.endian = params.get('endian', 'big').lower()
        
        if not self.endian in ['big', 'little']:
            raise ValueError("Protocol endianness should be either 'big' or 'little' (found '{e}')".format(e=self.endian))
        
        self.packet_suffix = params.get('packetSuffix', '_Packet_t')
        self.struct_suffix = params.get('structSuffix', '_t')