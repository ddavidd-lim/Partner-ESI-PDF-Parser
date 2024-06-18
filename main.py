import sys
sys.path.append('src')
import os 
import src.mapping as m
import src.classes
from src.classes.PDFReader import PDFReader as pdf_reader
from src.classes.Prompter import Prompter
from langchain_community.llms import Ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.documents import Document
import json

def parse_pdf(pdf_path):
  # Extract by Subsection
  subsection_dict = pdf_reader().process_file(pdf_path)

  # Extract datafields mapping from ESA File
  datafields = m.execute()
  
  # Initialize LLM
  llm = Ollama(model="phi3", temperature=0, num_predict=40, top_k=5, top_p=.3, mirostat_tau=0, format="json")
  # System Chat History
  #context_system_prompt = """Given a chat history and the latest question \
  #which might reference context in the chat history, answer the question. """
  context_system_prompt = """Retrieve the datafield defined in input within the context given. 
  Anything legal can be found in the context and chat history.
  If you cannot answer the question with the context, respond with N/A.

  <context>
  {context}
  </context>

  {input} is the prompt.
  Again, if you cannot answer the question respond N/A.
  Simply respond with only the answer that matches the datafield.
  There must only be one JSON object.
  Do not include the datafield in your response. Keep the key for the json exactly the same as the input.
  """
  # ChatPromptTemplate.from_template()

  context_prompt = ChatPromptTemplate.from_messages(
      [
          ("system", context_system_prompt),
          MessagesPlaceholder("chat_history", optional=True)#,
          ,("human", "{input}")
      ]
  )


  qa_system_prompt = context_system_prompt #"""Reading through a PDF and giving only the answers found within it. If you do not know an answer, you respond N/A."""


  qa_prompt = ChatPromptTemplate.from_messages(
      [
          ("system", qa_system_prompt),
          MessagesPlaceholder("chat_history")#,
          ,("human", "{input}")
      ]
  )


  qa_document_chain = qa_prompt | llm | JsonOutputParser()
  history_aware_retriever = context_prompt | llm | JsonOutputParser()
  retrieval_chain = create_retrieval_chain(
      history_aware_retriever, qa_document_chain)

  chat_history = []
  
  answers_dict = {}

  for subsection, field_to_questions in sorted(datafields.items()):
      subsection_answers = {}
      if subsection:      # (subsection == *selected section*)
          section_number = subsection.split('.')[0]
          for field, question in field_to_questions.items():
              try:
                  subsection_context = subsection_dict[section_number][subsection]
                  # -----------------------------INVOKE LLM---------------------------------------
                  output_dict = retrieval_chain.invoke({'input':question, 'context': [Document(page_content=subsection_context)], 
                                                      'chat_history':chat_history})
                  
                  # -----------------------------INVOKE LLM---------------------------------------
                  key = list(output_dict['answer'].keys())[0]
                  subsection_answers[question] = output_dict['answer'][key]
                  answer = subsection_answers[question]
                  print(f'> Answer: {answer}\n')
              except Exception as e:
                  print("!!!!!!!!!!!!!!!")
                  print(f'Error in Subsection {subsection}: {e}')
                  print("!!!!!!!!!!!!!!!")
      answers_dict[subsection] = subsection_answers
  # Write to JSON
  pdf_name = pdf_path.split('.')[0]
  with open(f"data/processed/{pdf_name}.json", "w") as outfile: 
      json.dump(answers_dict, outfile)
      
      
      
if __name__ == "__main__":
  pdf_path = "20-301704.3.pdf"
  
  parse_pdf(pdf_path)
  print("Done!")
