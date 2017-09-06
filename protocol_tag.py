class ProtocolTag:
    """ Simple class for xml tag functionality
    Protocol level tags should be defined here
    Alternative tags can be defined as a list
    """

    PROTOCOL = ["protocol"]
    REQUIRE = ["require", "req"]
    STRUCTURE = ["structure", "struct"]
    ENUM = ["enumeration", "enum"]
    DOC = ["documentation", "doc"]
    PACKET = ["packet", "pkt"]
    PREFIX = ["prefix"]
    
    @staticmethod
    def compare(tag, compare):
        tag = tag.lower()
        
        if type(compare) in [list, tuple]:
            return tag in compare
        
        return tag == compare
        
    @staticmethod
    def test_boolean(tag_value):
        """Value comparison function
        Takes a tag value and compares it to a list of possible true values
        """
        return str(tag_value).lower() in ['y', 'yes', '1', 'true', 'on']
        
        
    @staticmethod
    def is_tag_present(xml_node, tag_name):
        return tag_name in xml_node.attrib
        
        
    @staticmethod
    def is_tag_set(xml_node, tag_name):
        """Return true if the value of the given tag is set 
        to one of the allowed boolean values
        """
        tag = xml_mode.attrib.get(tag_name, '')
        return test_boolean(tag)