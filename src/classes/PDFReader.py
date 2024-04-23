import fitz
import re
import os
from typing import List, Tuple, Dict
from .Section import Section

class PDFReader:
	def extract_by_section(self, pages: List[Tuple[str, List[str]]]) -> List[Section]:
		"""_summary_
		Takes in a list of pages where each list contains the page number and a list of lines in that page.
  
		Args:
			pages (List[Tuple[str, List[str]]]): structured as: [('1', [line1, line2, ...]]

		Returns:
			List[Section]: List of Section objects
		"""

		sections = []
		current_section = None
		section_found	= False
		for page, lines in pages:
			for line in lines[4:]:
				#print("printing line --------------------------------------------------------------------------------")
				#print(line)
				#print("done--------------------------------------------------------------------------")
				# Split section num from line
				split_line = line.split()
				#print(split_line)
				section_num = split_line[0]
				#print('NEW SECTION FOUND:', section_num)
				if section_num.endswith(".0"):
					if current_section:
						sections.append(current_section)
					current_section = Section()
					current_section.section_num = line
					section_found = True
				# Check if the title is in the same line as the section number
				if len(split_line) >= 2:
					current_section.section_title = ' '.join(split_line[1:])
					# for word in split_line[1:]:
					# 	current_section.section_title += word
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


	def extract_subsections(self, sections: List[Section]) -> 'Dict{int: Dict{int: Section}}':
		"""_summary_
		Takes in a list of Sections, where each Section contains the section number, section title, and section text 
		  where each text is a list of lines. 
	
		 This returns a dictionary, mapping each subsection to a list of Sections 
	   There is an additional parameter in Section called paragraph, which needs to be filled for each subsection. 

		Args:
			sections (List[Section]): List of Section objects

		Returns:
			Dict{int: Dict{int: Section}}: Dictionary containing main section number as key,
											List of subsection dicts as value
		"""
		# for section in sections: 
		# 	for line in section.text: 
		# 		print(line, '\n\n')
		section_map = dict()
		current_subsection = None
		nextLineTitle = False
		
		for section in sections: 
			#print('NEW SECTION --------------------------------------------------')
			#print(section.text)
			#print('DONE---------------------------------------------')
			section_num = section.section_num[0]
			subsections = {} # This is a dictionary mapping subsection to text
			for line in section.text:
				if line.strip().startswith(section_num):
					if current_subsection:
						#subsections.append(current_subsection) CHANGE
						subsections[current_subsection.section_num] = current_subsection.paragraph # saying that if there is a current section, store that in the dictionary
																							  # before making a new one  
					current_subsection = Section()
					current_subsection.section_num = line.split()[0]
					
					# Check if the title is in the same line as the section number
					if len(line.strip()) >= 2:
						current_subsection.section_title = ' '.join(line.split()[1:])
						# CHANGE: COMMENTED THIS OUT 
						# for word in subsection_number[0:]: 
						#	 current_subsection.section_title += word
						nextLineTitle = False
					else:
						current_subsection.section_num = line
						nextLineTitle = True
						continue

				if nextLineTitle:
					current_subsection.section_title = ' '.join(line)
					nextLineTitle = False
				else:
					current_subsection.paragraph += ' ' + line
			#subsections.append(current_subsection)
			subsections[current_subsection.section_num] = current_subsection.paragraph
			section_map[section_num] = subsections
			current_subsection = None

		# for section in section_map: 
		# 	print(section_map[section]) #for line in section.text: 
		#  		#print(line, '\n\n')

		return section_map


	def remove_table_of_contents(self, pages):
		return [i for i in pages if i[0] != ""]
	
	def section_to_text(self, subsection_dict):
		subsection_texts = {}
		#print(subsection_dict.items())
		for section, subsections in subsection_dict.items():
			for subsection in subsections:
				# print(f"------{subsection.section_num} + {type(subsection.section_num)}------")
				#subsection_texts[subsection.section_num] = (' '.join(subsection.text))
				pass
		return subsection_texts


	def process_file(self, filename:str) -> Dict[str, str]:
		"""

		Args:
			filename (str): the name of the file

		Returns:
			Dict{int: Dict{int: Section}}: A dictionary that maps main section number to a dict of its subsections
		"""
		print('here')
		current_directory = os.path.dirname(os.path.abspath(__file__))
		pdf_name = filename
		pdf_path = os.path.join(current_directory, "..", "..", "data","raw", pdf_name)
		print(pdf_path)
		output_path = os.path.join(current_directory, "..",	"..", "data","processed", "output.txt")
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
		with open(output_path, 'r', encoding='utf8') as file:
			page = []
			for line in file:
				#print(line)
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
		print("extracing by section .......................................................................................")
		sections = self.extract_by_section(content)
		section_map = self.extract_subsections(sections)

		print("Section Map: ", section_map)
		return section_map
	
	