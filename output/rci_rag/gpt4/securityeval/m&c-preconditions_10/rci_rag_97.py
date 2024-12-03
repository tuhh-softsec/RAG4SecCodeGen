import os
from lxml import etree
from defusedxml.lxml import parse
from defusedxml.lxml import XMLParser as DefusedXMLParser
import logging
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_root(schema_path='resources/config.xsd'):
    '''
    Create an XML parser, parse the XML schema file, and return an XMLSchema.
    This function uses defusedxml to mitigate XML attacks.
    '''
    # Use defusedxml to parse the XML file securely
    parser = DefusedXMLParser(no_network=True, remove_comments=True, remove_pis=True)

    # Ensure the XML schema file exists and is not writable by unauthorized users
    if not os.path.exists(schema_path):
        logger.error(f"Schema file {schema_path} does not exist.")
        return None
    if not os.access(schema_path, os.R_OK):
        logger.error(f"Schema file {schema_path} is not readable.")
        return None
    if (os.access(schema_path, os.W_OK) and
        (os.stat(schema_path).st_mode & (0o222 | 0o020))):
        logger.error(f"Schema file {schema_path} has insecure permissions.")
        return None

    # Verify the integrity of the schema file
    expected_hash = "EXPECTED_SHA256_HASH"
    with open(schema_path, 'rb') as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()
    if actual_hash != expected_hash:
        logger.error(f"Schema file {schema_path} integrity check failed.")
        return None

    # Parse the XML schema file securely
    try:
        xmlschema_doc = parse(schema_path, parser=parser)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        return xmlschema
    except etree.XMLSchemaParseError as e:
        logger.error(f"Error parsing XML Schema: {e}")
        return None
    except etree.XMLSyntaxError as e:
        logger.error(f"XML Syntax Error: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

# Example usage
xmlschema = get_root()
if xmlschema is not None:
    logger.info("XMLSchema successfully parsed and returned.")
else:
    logger.error("Failed to parse XMLSchema.")

