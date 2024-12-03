from lxml import etree
from defusedxml.lxml import parse

def transform_xml():
    '''
    Create a secure XML parser, parse the 'resources/config.xsl' file,
    and return an XSLT object.
    '''
    # Use defusedxml to parse the XSL file securely
    xsl_doc = parse('resources/config.xsl')
    xsl_transformer = etree.XSLT(xsl_doc)
    
    return xsl_transformer

# Example usage
if __name__ == "__main__":
    # Obtain the XSLT transformer object
    transformer = transform_xml()
    
    # Example of how to use the transformer with an XML document
    # xml_doc = parse('resources/input.xml')  # Securely parse an XML input
    # result = transformer(xml_doc)
    # print(str(result))

