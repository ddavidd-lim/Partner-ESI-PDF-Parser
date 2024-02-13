class Section():
  """
  This class is meant to store the section number, title, and text of the
  section/subsection
  """
  def __init__(self):
    self.section_num = "0"
    self.section_title = ""
    self.text = []

  def __str__(self):
    return f"Section {self.section_num} {self.section_title}:"

  def display_text(self):
    for t in self.text:
      print(t)
