import os
import yaml
import logging
from yaml import YAMLError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def yaml_load(filename, base_path=None):
    '''
    Securely load the contents of a YAML file, ensuring that the file is within a specified directory.
    
    :param filename: The path to the YAML file to be loaded.
    :param base_path: The base directory from which the file should be loaded. If None, uses current directory.
    :return: The parsed YAML data.
    :raises ValueError: If the file path is invalid or outside the intended directory.
    :raises FileNotFoundError: If the file does not exist.
    :raises PermissionError: If the file cannot be accessed due to permissions.
    :raises yaml.YAMLError: If there is an error parsing the YAML content.
    '''
    # Validate and sanitize the file path
    if base_path is None:
        base_path = os.getcwd()
    full_path = os.path.abspath(os.path.join(base_path, filename))
    if not full_path.startswith(os.path.abspath(base_path)):
        logging.error(f"Attempted directory traversal attack with filename: {filename}")
        raise ValueError("Invalid file path.")

    if not os.path.isfile(full_path):
        logging.error(f"File not found: {full_path}")
        raise FileNotFoundError(f"The file {full_path} does not exist.")
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            # Use safe_load to avoid executing arbitrary code
            data = yaml.safe_load(file)
            return data
    except (FileNotFoundError, PermissionError) as e:
        logging.error(f"File access error: {e}")
        raise
    except YAMLError as e:
        logging.error(f"YAML parsing error: {e}")
        raise YAMLError(f"Error parsing YAML file: {e}")

# Example usage:
try:
    data = yaml_load('example.yaml', base_path='/path/to/allowed/directory')
    print(data)
except (ValueError, FileNotFoundError, PermissionError, YAMLError) as e:
    print(f"An error occurred: {e}")

