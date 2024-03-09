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
		"""
        Return a view object that displays a list of a given dictionary's key-value pairs as tuples.

        Returns:
            dict_items: A view object that displays a list of a given dictionary's key-value pairs as tuples.
        """
		return self.fields.items()

	def add_datafield(self, section_num, datafield, value):
		"""
        Add a datafield mapping to the specified section number.

        Args:
            section_num (int): The section number to which the datafield mapping will be added.
            datafield (str): The datafield key.
            value (str): The question value associated with the datafield.

        Raises:
            ValueError: If the specified section number does not exist.
        """
		if section_num in self.fields:
				self.fields[section_num][datafield] = value
		else:
				raise ValueError("Section does not exist.")
