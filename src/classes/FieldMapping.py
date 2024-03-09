class FieldMapping:
	def __init__(self):
		self.fields = dict()
  
	def items(self):
		return self.fields.items()

	def add_datafield(self, section_num, datafield, value):
			if section_num in self.fields:
					self.fields[section_num][datafield] = value
			else:
					raise ValueError("Section does not exist.")
