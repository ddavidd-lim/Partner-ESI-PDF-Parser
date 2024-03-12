import fitz
import re
import os
from typing import List, Tuple, Dict
from classes.Section import Section

class PDFReader:
  def extract_by_section(self, pages: List[Tuple[str, List[str]]]) -> List[Section]:
    """_summary_

    Args:
      pages (List[Tuple[str, List[str]]]): structured as: [('1', [line1, line2, ...]]

    Returns:
      List[Section]: List of Section objects
    """
    
    sections = []
    current_section = None
    section_found  = False
    for page, lines in pages:
      for line in lines[4:]:
        # Split section num from line
        split_line = line.split()
        section_num = split_line[0]
        if section_num.endswith(".0"):
          if current_section:
            sections.append(current_section)
          current_section = Section()
          current_section.section_num = line
          section_found = True
        # Check if the title is in the same line as the section number
        if len(split_line) >= 2:
          for word in split_line[1:]:
            current_section.section_title += word
          nextLineTitle = False
        else:
          nextLineTitle = True
        
        # Process lines other than section num
        if nextLineTitle:
          current_section.section_title = line
          nextLineTitle = False
        if section_found:
          current_section.text.append(line)
    return sections


  def extract_subsections(self, sections: List[Section]) -> Dict[int, List[Section]]:
    """_summary_

    Args:
      sections (List[Section]): List of Section objects

    Returns:
      Dict[int, List[Section]]: Dictionary containing main section number as key,
                    List of subsections as value
    """
    section_map = dict()
    current_subsection = None
    nextLineTitle = False
    
    for section in sections:
      section_num = section.section_num[0]
      subsections = []
      for line in section.text:
        if line.startswith(section_num):
          if current_subsection:
            subsections.append(current_subsection)
          current_subsection = Section()
          subsection_number = line.split()
          current_subsection.section_num = subsection_number[0]
          
          # Check if the title is in the same line as the section number
          if len(subsection_number) >= 2:
            for word in subsection_number[1:]:
              current_subsection.section_title += word
            nextLineTitle = False
          else:
            current_subsection.section_num = line
            nextLineTitle = True
            continue

        if nextLineTitle:
          current_subsection.section_title = line
          nextLineTitle = False
        else:
          current_subsection.text.append(line)
      subsections.append(current_subsection)
      section_map[int(section_num)] = subsections
      current_subsection = None

    return section_map


  def remove_table_of_contents(self, pages):
    return [i for i in pages if i[0] != ""]
  
  def section_to_text(self, subsection_dict):
    subsection_texts = {}
    for section, subsections in subsection_dict.items():
        for subsection in subsections:
            # print(f"------{subsection.section_num} + {type(subsection.section_num)}------")
            subsection_texts[subsection.section_num] = (' '.join(subsection.text))
    return subsection_texts


  def process_file(self, filename:str) -> Dict[str, str]:
    """

    Args:
      filename (str): the name of the file

    Returns:
      Dict[int, List[Section]]: A dictionary that maps main section number to a list of its subsections
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pdf_name = filename
    pdf_path = os.path.join(current_directory, "..", "..", "data","raw", pdf_name)
    output_path = os.path.join(current_directory, "..",  "..", "data","processed", "output.txt")
    doc = fitz.open(pdf_path)
    out = open(output_path, "wb")
    for page in doc:
      text = page.get_text().encode("utf8")
      out.write(text)
      out.write(bytes((12,)))
    out.close()
    doc.close()


    pattern = r'Page\s+([\d]+)'
    pages = []
    page_num = ""
    with open(output_path, 'r', encoding='utf8') as f:
      page = []
      for line in f:
        if line.strip() != "":
          page.append(line.strip())
        matches = re.findall(pattern, line)
        if len(matches) > 0:
          page_num = matches[0]
        if '\f' in line:
          pages.append((page_num, page))
          page = []
          page_num = ""

    content = self.remove_table_of_contents(pages)
    sections = self.extract_by_section(content)
    section_map = self.extract_subsections(sections)
    
    return self.section_to_text(section_map)
  
  