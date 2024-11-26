import os
import zipfile
from pathlib import Path

# Define the path to the archive and the extraction directory
archive_path = 'archive.zip'
extraction_dir = Path('/tmp/unpack')

# Ensure the extraction directory exists
os.makedirs(extraction_dir, exist_ok=True)

# Open the archive.zip file as a zipfile
with zipfile.ZipFile(archive_path, 'r') as zip_ref:
    # Extract all files from the archive to the /tmp/unpack directory
    # We will check each file to ensure it does not escape the extraction directory
    for file_info in zip_ref.infolist():
        # Security check to prevent directory traversal attacks
        extracted_path = extraction_dir / file_info.filename
        if not extracted_path.resolve().parent == extraction_dir.resolve():
            raise Exception(f"Detected a potential directory traversal attack: {file_info.filename}")
        
        # Extract the file
        zip_ref.extract(file_info, extraction_dir)

print("Extraction complete.")

