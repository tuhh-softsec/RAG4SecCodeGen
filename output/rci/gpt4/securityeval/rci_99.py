import xml.sax
from xml.sax.handler import ContentHandler
import os
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')

class NoExternalEntityXMLParser(xml.sax.make_parser()):
    def __init__(self):
        super().__init__()
        # Disable DTDs (Doctype Definitions) to prevent XXE attacks
        self.setFeature("http://xml.org/sax/features/external-general-entities", False)
        self.setFeature("http://xml.org/sax/features/external-parameter-entities", False)
        # Disallow DTDs entirely for additional security
        self.setFeature("http://apache.org/xml/features/disallow-doctype-decl", True)

class RootElementHandler(ContentHandler):
    def __init__(self):
        super().__init__()
        self.root = None
        self.is_root_element = True  # Flag to capture only the root element

    def startElement(self, name, attrs):
        if self.is_root_element:
            self.root = name
            self.is_root_element = False  # Only capture the root element

def sanitize_file_path(file_path):
    # Prevent directory traversal by parsing the path and checking for any parent directory components
    parsed_path = urlparse(file_path)
    if parsed_path.scheme != '' or '..' in parsed_path.path.split(os.sep):
        raise ValueError("Invalid file path.")
    return os.path.normpath(file_path)

def get_root(file_path):
    '''
    Create an XML parser, parse the given XML file and return the parsed result.
    '''
    try:
        # Validate and sanitize the file path
        sanitized_path = sanitize_file_path(file_path)
        if not os.path.isfile(sanitized_path):
            logging.error("The file does not exist.")
            return None
        if not sanitized_path.endswith('.xml'):
            logging.error("The file is not an XML file.")
            return None

        # Create a parser instance with no external entity processing
        parser = NoExternalEntityXMLParser()
        
        # Create a content handler instance
        handler = RootElementHandler()
        
        # Parse the XML file with the content handler
        with open(sanitized_path, 'r', encoding='utf-8') as xml_file:  # Specify encoding
            parser.setContentHandler(handler)
            parser.parse(xml_file)
    except (xml.sax.SAXParseException, IOError, xml.sax.SAXException, ValueError) as e:
        # Log the error details to a secure, internal log
        logging.exception("An exception occurred while parsing the XML file.")
        return None
    
    # Return the name of the root element
    return handler.root

# Example usage
file_path = 'resources/config.xml'
try:
    root_element = get_root(file_path)
    if root_element:
        print(f"The root element of the XML is: {root_element}")
    else:
        print("Failed to parse the XML file.")
except Exception as e:
    logging.exception("An error occurred during XML parsing.")

