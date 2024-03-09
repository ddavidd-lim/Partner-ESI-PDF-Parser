class FieldMapping:
	"""
		An abstraction of a dictionary which maps section_num to its mappings of fields within
		that section
  
		key   = section_num: int
		value = mapping: dict
				key   = datafield: str
				value = question: str
	"""
	def __init__(self):
		self.fields = dict()
  
	def items(self):
		return self.fields.items()

	def add_datafield(self, section_num, datafield, value):
			if section_num in self.fields:
					self.fields[section_num][datafield] = value
			else:
					raise ValueError("Section does not exist.")
