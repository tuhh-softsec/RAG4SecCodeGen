from defusedxml.lxml import parse

def get_root():
    '''
    Create an XML parser, parse the 'resources/config.xml' file and return the root.
    '''
    # Ensure the file path is secure and does not contain any dangerous patterns
    # Since the file path is static and known to be safe, we can skip dynamic validation in this case.
    file_path = 'resources/config.xml'

    # Parse the XML file securely
    try:
        # Open the file using a context manager to ensure it's closed properly
        with open(file_path, 'rb') as xml_file:
            # Parse the XML file with defusedxml to prevent XML attacks
            xml_tree = parse(xml_file)
            # Get the root of the XML tree
            root = xml_tree.getroot()
            return root
    except IOError as e:
        # Handle file I/O errors (e.g., file not found)
        print(f"An error occurred while trying to read the file: {e}")
        return None
    except etree.XMLSyntaxError as e:
        # Handle XML parsing errors
        print(f"An error occurred while parsing the XML file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    root = get_root()
    if root is not None:
        print(f"The root element is: {root.tag}")
    else:
        print("Failed to get the root element.")

