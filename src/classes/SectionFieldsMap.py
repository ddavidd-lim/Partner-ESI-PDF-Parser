class SectionFieldsMap:
    """
        An abstraction of a dictionary which maps section_num to its mappings of fields within
        that section
  
        key   = section_num: int
        value = mapping: dict
                key   = datafield: str
                value = question: str
    """
    def __init__(self, fields):
        self.fields = fields
  
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
                self.fields[section_num] = {datafield: value}
    
    def get_section_fields(self, section_num):
        """
        Retrieve the fields mapping for the specified section number.

        Args:
            section_num (int): The section number for which to retrieve the fields mapping.

        Returns:
            dict: A dictionary containing the fields mapping for the specified section number.

        Raises:
            ValueError: If the specified section number does not exist in the fields mapping.
        """
        try:
           return self.fields[section_num]
        except:
            return None
        
        # if section_num in self.fields:
        #         return self.fields[section_num]
        # else:
        #         raise ValueError("Section number does not exist")
