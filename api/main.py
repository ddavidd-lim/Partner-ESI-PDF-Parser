import json
from pathlib import Path
import random

output_directory = Path('.') / 'output'

def process_filename(file):
    name = file.name.removeprefix("output")
    return name[:name.find('.')] if '.' in name else name

def main():
    files_in_current = [process_filename(file) for file in output_directory.iterdir() if file.is_file()]
    last_index_file = int(max(files_in_current,default=0)) + 1
    new_file_name = "output" + str(last_index_file) + ".json" 
    new_file_path = output_directory / new_file_name
    try:
        with open(new_file_path,'x') as file:
            file.write(str(random.randint(0,100)))
    except:
        print("ERRORR ALERT")

    return new_file_path.absolute()
    
if __name__ == "__main__":
    print(main())