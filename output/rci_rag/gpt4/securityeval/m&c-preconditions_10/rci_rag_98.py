import logging
from lxml import etree
from defusedxml.lxml import parse, fromstring
import os

# Configure logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def transform_xml(xsl_file_path):
    '''
    Create a secure XML parser, parse the XSL file,
    and return an XSLT object.
    '''
    try:
        # Validate file path
        if not os.path.isfile(xsl_file_path):
            raise ValueError("Invalid file path")

        # Use defusedxml to parse the XSL file securely
        xsl_doc = parse(xsl_file_path)
        xsl_transformer = etree.XSLT(xsl_doc)
        return xsl_transformer
    except (etree.XMLSyntaxError, ValueError) as e:
        # Log parsing errors
        logging.error(f"Error parsing XSL file: {e}")
        return None

def parse_xml_securely(file_path):
    '''
    Parse an XML file securely using defusedxml.
    '''
    try:
        # Validate file path
        if not os.path.isfile(file_path):
            raise ValueError("Invalid file path")

        # Disable DTD (Document Type Definition) to prevent entity expansion attacks
        parser = etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=False)
        
        # Use a context manager to ensure the file is properly closed
        with open(file_path, 'rb') as file:
            xml_doc = fromstring(file.read(), parser=parser)
        return xml_doc
    except (etree.XMLSyntaxError, ValueError) as e:
        # Log parsing errors
        logging.error(f"Error parsing XML file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    try:
        # Transform XML securely
        xsl_file_path = 'resources/config.xsl'
        transformer = transform_xml(xsl_file_path)
        if transformer is not None:
            # Assume 'input.xml' is an XML file to be transformed
            xml_file_path = 'input.xml'
            xml_doc = parse_xml_securely(xml_file_path)
            if xml_doc is not None:
                result = transformer(xml_doc)
                
                # Output the result to a string with proper encoding
                result_str = etree.tostring(result, encoding='unicode', method='xml')
                
                # Securely handle the result, e.g., store it in a secure manner if it contains sensitive data
                # Implement access control, logging, and monitoring as needed by the application
                # Validate file paths and follow secure deployment practices
    except Exception as e:
        # Log any other errors that may occur
        logging.error(f"An unexpected error occurred: {e}")

