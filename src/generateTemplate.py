import os

import sys
sys.path.append('../src/')
import ReadPDF as rdpdf
from flagEntities import flagText
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline


if __name__ == "__main__":
  filename = input("Input PDF Report filename (ex. Partner.pdf): ")
  subsection_map = rdpdf.process_file(filename=filename)  # Dict[int, List[Section]]
  
  
  current_directory = os.path.dirname(os.path.abspath(__file__))
  output_path = os.path.join(current_directory, "..", "data","processed", "flagged_text.txt")
  out = open(output_path, "w", encoding="utf-8")
  
  # Load NLP
  tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
  model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
  nlp = pipeline("ner", model=model, tokenizer=tokenizer)
  
  for section_num, subsections in subsection_map.items():
    for section in subsections:
      section_text = "\n".join(section.text)
      text = flagText(nlp, section_text)
      out.write(f"{section.section_num}\n")
      out.write(f"{section.section_title}\n")
      out.write(f"{text}\n")
      
  out.close()
      