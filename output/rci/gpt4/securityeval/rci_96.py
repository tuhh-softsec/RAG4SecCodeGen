import os
import logging
from logging.handlers import RotatingFileHandler
from lxml import etree
from lxml.etree import XMLParser

# Configure logging with rotation
log_file_path = 'app.log'
logger = logging.getLogger('xml_parser')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=3)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def is_safe_path(base_path, path, follow_symlinks=True):
    # Resolve and check if path is within base_path
    if follow_symlinks:
        return os.path.realpath(path).startswith(base_path)
    else:
        return os.path.abspath(path).startswith(base_path)

def get_root(xml_file_path):
    '''
    Create an XML parser with security features enabled, parse the XML file and return the root.
    '''
    # Define secure parser configuration
    parser = XMLParser(no_network=True, remove_blank_text=True, resolve_entities=False, huge_tree=False, collect_ids=False)
    
    # Validate and sanitize the XML file path
    base_path = os.path.abspath('resources')  # Define the base directory for XML files
    if not is_safe_path(base_path, xml_file_path):
        logger.error(f"Unsafe file path: {xml_file_path}")
        return None

    if not os.path.isfile(xml_file_path):
        logger.error(f"File not found: {xml_file_path}")
        return None

    # Check for file access permissions
    if not os.access(xml_file_path, os.R_OK):
        logger.error(f"File not readable: {xml_file_path}")
        return None

    try:
        # Parse the XML file using the secure parser
        tree = etree.parse(xml_file_path, parser)
        # Get the root element of the XML file
        root = tree.getroot()
        return root
    except etree.XMLSyntaxError as e:
        logger.error(f"XML Syntax Error: {e}")
        return None
    except IOError as e:
        logger.error(f"IO Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

# Example usage
xml_file_path = os.path.join('resources', 'config.xml')  # Use os.path.join to construct the file path
root = get_root(xml_file_path)
if root is not None:
    logger.info("XML root element obtained successfully.")
else:
    logger.error("Failed to obtain XML root element.")

