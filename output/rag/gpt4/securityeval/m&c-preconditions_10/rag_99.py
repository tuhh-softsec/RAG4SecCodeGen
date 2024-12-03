from defusedxml.sax import parse

class SecureXMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.root = None

    def startElement(self, name, attrs):
        if self.root is None:
            self.root = name

def get_root():
    '''
    Create an XML parser,
    parse the file 'resources/config.xml' and return the parsed result.
    '''
    # Instantiate the secure XML handler
    handler = SecureXMLHandler()
    
    # Parse the XML file securely
    with open('resources/config.xml', 'r') as xml_file:
        parse(xml_file, handler)
    
    # Return the root element name
    return handler.root

# Ensure that the defusedxml package is installed
# pip install defusedxml

# Example usage
if __name__ == "__main__":
    root_element = get_root()
    print(f"The root element of the XML is: {root_element}")

