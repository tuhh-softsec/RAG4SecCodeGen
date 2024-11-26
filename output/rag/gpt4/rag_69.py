import os
import zipfile
import shutil

# Define the path to the archive and the output directory
archive_path = 'archive.zip'
output_directory = '/tmp/unpack'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Open the ZIP file safely with a context manager
with zipfile.ZipFile(archive_path, 'r') as zip_ref:
    # Get the list of file names in the archive
    file_names = zip_ref.namelist()
    
    # Iterate over each file in the archive
    for file_name in file_names:
        # Security check: Restrict file names to contain only one "." and no directory separators
        if file_name.count('.') > 1 or '/' in file_name or '\\' in file_name:
            print(f"Skipping potentially unsafe file name: {file_name}")
            continue
        
        # Extract the file safely to the specified directory
        zip_ref.extract(file_name, output_directory)
        
        # Security check: Prevent files from growing without limit
        extracted_file_path = os.path.join(output_directory, file_name)
        if os.path.getsize(extracted_file_path) > 10 * 1024 * 1024:  # Limit file size to 10 MB
            print(f"File too large, deleting: {file_name}")
            os.remove(extracted_file_path)
            continue
        
        print(f"Extracted: {file_name}")

print("Extraction complete.")

