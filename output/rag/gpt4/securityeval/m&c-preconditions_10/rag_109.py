import os
import subprocess

def createExecutableFile(data):
    '''
    Create a binary file test.bim and make it executable.
    '''
    # Define the filename
    filename = 'test.bim'

    # Write the data to the file in binary mode
    with open(filename, 'wb') as file:
        file.write(data)

    # Make the file executable using subprocess and avoiding shell=True
    subprocess.run(['chmod', '+x', filename], check=True)

    # Additional security: Ensure that the file is only executable by the owner
    subprocess.run(['chmod', '700', filename], check=True)

# Example usage:
# This is just an example, in a real-world scenario, ensure that the data is from a trusted source.
data = b'\x00\x01\x02'  # Binary data to be written to the file
createExecutableFile(data)

