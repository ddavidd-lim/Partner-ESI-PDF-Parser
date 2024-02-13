# reading from output_text.txt
# find the sections we need to transfer
# copy the text in the section to the copied word doc

import shutil

def copy_word_document(original_path, copy_path):
    try:
        shutil.copy2(original_path, copy_path)
        print(f"Copy successful! {original_path} copied to {copy_path}")
    except FileNotFoundError:
        print(f"Error: The original file {original_path} was not found.")
    except PermissionError:
        print(f"Error: Permission denied. Unable to copy {original_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
original_document_path = './data/raw/21-342562.35_Training_Report.docx'
copy_document_path = 'output/21-342562.35_Generated_Report.docx'

copy_word_document(original_document_path, copy_document_path)
