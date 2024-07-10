import zipfile
import os

# Path to the zip file
zip_file_path = 'Outlook for Mac Archive.olm'

# Directory to extract the Calendar.xml file to (same as the directory containing the zip file)
extract_to_directory = os.path.dirname(os.path.abspath(zip_file_path))

# Open the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # List all files in the zip archive
    all_files = zip_ref.namelist()
    
    # Search for the Calendar.xml file
    for file in all_files:
        # Check if the file path matches the expected pattern
        if file.endswith('Calendar/Calendar.xml'):
            # Extract the Calendar.xml file to the root directory
            zip_ref.extract(file, extract_to_directory)
            # Move the extracted file to the root directory
            extracted_file_path = os.path.join(extract_to_directory, file)
            new_file_path = os.path.join(extract_to_directory, 'Calendar.xml')
            os.rename(extracted_file_path, new_file_path)
            print(f'Extracted {file} to {new_file_path}')

# Print confirmation
print(f'Calendar.xml has been extracted to {new_file_path}')
