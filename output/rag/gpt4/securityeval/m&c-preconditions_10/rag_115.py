from defusedxml.lxml import parse

def getXmlRoot():
    '''
    Create an XML parser and parse the resources/c.xml file and return the root element
    '''
    # Open the XML file securely
    with open('resources/c.xml', 'rb') as xml_file:
        # Parse the XML file using defusedxml to prevent XML attacks
        xml_tree = parse(xml_file)
        # Get the root element of the XML tree
        root = xml_tree.getroot()
        return root

# Example usage
if __name__ == "__main__":
    root = getXmlRoot()
    print(root.tag)  # Prints the tag of the root element

