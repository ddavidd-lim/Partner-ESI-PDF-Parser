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

original_document_path = './data/raw/21-342562.35_Training_Report.docx'
copy_document_path = 'output/21-342562.35_Generated_Report.docx'
copy_word_document(original_document_path, copy_document_path)



def get_section(start_section, end_section):
    # TODO: optimize logic to one loop
    # TODO: track start:stop sections in dict
    file_path = "output/output_text.txt"

    i = 0
    sections = []
    with open(file_path, 'r') as file:
        for line in file:
            i += 1
            if start_section in line:
                sections.append(i)
                print(line, i)
            if end_section in line:
                sections.append(i)
        sections = sections[2:]
        print(sections)
        print()

    section_lines = ""  
    with open(file_path, 'r') as file:
            for i, line in enumerate(file, start=1):
                if sections[0]+1 < i < sections[1]:
                    section_lines += line
    print(section_lines)

start_section = input("Section to transfer: ")
end_section = input("Next Section: ")
get_section(start_section, end_section)