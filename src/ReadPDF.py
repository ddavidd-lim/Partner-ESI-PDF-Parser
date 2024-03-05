#!/usr/bin/env python
# coding: utf-8


import fitz
import re
from typing import List, Tuple, Dict
import os

import sys
sys.path.append('../src/')
from classes.Section import Section

def select_Section(sections, section_num) -> str:
	try:
		list_section_text = ['\n'.join(section.text) for section in sections] 
		return list_section_text[section_num - 1]
	except:
		return ValueError("Section out of bounds.")

def select_Subsection(subsection_dict, section_num, subsection) -> str:
	try:
		return ' '.join(subsection_dict[section_num][subsection].text)
	except:
		return ValueError("Subsection out of bounds.")

def extract_by_section(pages: List[Tuple[str, List[str]]]) -> List[Section]:
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
				continue
			else:
				nextLineTitle = True
				continue
			
			# Process lines other than section num
			if nextLineTitle:
				current_section.section_title = line
				nextLineTitle = False
			if section_found:
				current_section.text.append(line)
	return sections


def extract_subsections(sections: List[Section]) -> Dict[int, List[Section]]:
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


def display_all_sections(sections, displayText):
	for section in sections:
		print("--------------------------------------------------------------------------------------")
		print(f"> Section number: {section}")
		print(f"- Title: {section.section_title}")
		if displayText:
			section.display_text()


def display_all_subsections(section_map, displayText):
	for section in section_map.keys():
		print("--------------------------------------------------------------------------------------")
		for subsection in section_map[section]:
			print(f"> Section number: {section}")
			print(f"- Subsection number: {subsection.section_num}")
			print(f"- Title: {subsection.section_title}")
			if displayText:
				subsection.display_text()


def display_one_section(sections: List[Section], section_num):
	print(f"Section number: {sections[section_num].section_num}")
	print(f"Title: {sections[section_num ].section_title}")
	sections[section_num].display_text()


def display_one_sub_section(subsections: Dict[int, List[Section]], section_num, subsection_index):
	print(f"Section number: {section_num}")
	print(f"Subsection number: {subsections[section_num][subsection_index].section_num}")
	print(f"Title: {subsections[section_num ][subsection_index].section_title}")
	subsections[section_num][subsection_index].display_text()


def remove_table_of_contents(pages):
	return [i for i in pages if i[0] != ""]



def process_file(filename:str) -> Dict[int, List[Section]]:
	"""_summary_

	Args:
		filename (str): the name of the file

	Returns:
		Dict[int, List[Section]]: A dictionary that maps main section number to a list of its subsections
	"""
	current_directory = os.path.dirname(os.path.abspath(__file__))
	pdf_name = filename
	pdf_path = os.path.join(current_directory, "..", "data","raw", pdf_name)
	output_path = os.path.join(current_directory, "..", "data","processed", "output.txt")
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

	content = remove_table_of_contents(pages)
	sections = extract_by_section(content)
	section_map = extract_subsections(sections)
	
	return section_map

def process_into_sections(filename:str) -> List[Section]:
	current_directory = os.getcwd()
	pdf_name = filename
	pdf_path = os.path.join(current_directory, "..", "data","raw", pdf_name)
	output_path = os.path.join(current_directory, "..", "data","processed", "output.txt")
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
	
	content = remove_table_of_contents(pages)
	sections = extract_by_section(content)
	return sections
