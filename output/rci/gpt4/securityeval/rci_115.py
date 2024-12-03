import os
import logging
from lxml import etree
from lxml.etree import XMLParser, ParseError, LxmlError, XMLSyntaxError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_safe_path(base_path, path, follow_symlinks=False):
    # Resolve the canonical path of the target and base
    base_path = os.path.realpath(base_path) if follow_symlinks else os.path.abspath(base_path)
    path = os.path.realpath(path) if follow_symlinks else os.path.abspath(path)
    # Ensure the target path starts with the base path
    return os.path.commonpath([base_path]) == os.path.commonpath([base_path, path])

def getXmlRoot(xml_file_path='resources/c.xml', base_path='.'):
    '''
    Create an XML parser with security features enabled, parse the XML file,
    and return the root element.
    '''
    # Ensure the file path is safe
    if not is_safe_path(base_path, xml_file_path):
        raise ValueError("Unsafe file path detected")

    # Create a secure XML parser
    parser = XMLParser(no_network=True, remove_blank_text=True, resolve_entities=False, huge_tree=False)
    
    try:
        # Parse the XML file using the secure parser
        with open(xml_file_path, 'rb') as xml_file:
            tree = etree.parse(xml_file, parser)
        # Get the root element of the XML file
        root = tree.getroot()
        return root
    except (ParseError, LxmlError, XMLSyntaxError, IOError) as e:
        # Log the error without exposing sensitive information
        logger.error(f"Error parsing XML: {type(e).__name__}")
        return None

# Example usage
if __name__ == "__main__":
    try:
        root = getXmlRoot()
        if root is not None:
            print(etree.tostring(root, pretty_print=True).decode())
    except ValueError as e:
        logger.error(f"Error: {e}")

