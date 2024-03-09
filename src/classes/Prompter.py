from langchain_community.llms import Ollama
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

class Prompter:
    def __init__(self):
        llm = Ollama(model="phi", temperature=0, num_predict=40, top_k=5, top_p=.5, mirostat_tau=0, format="json")
        json_parser = JsonOutputParser()
        prompt = PromptTemplate.from_template("""Retrieve the datafield defined in input within the context given.
                Anything legal can be found in the context.
                
                <context>
                {context}
                </context>
                
                {input} is the key in the dictionary where the value is the prompt for the datafield.
                Simply respond with only the answer that matches the datafield.
                There must only be one item in the dictionary.
                Keep the key for the json exactly the same as the input.
                """)
        self.model_chain = create_stuff_documents_chain(llm, prompt, output_parser=json_parser)
    
    def invoke(self, prompt, context):
        json = self.model_chain.invoke({
          "input": str(prompt),
          "context": [Document(page_content=context)]
          })
        return json

    def extract_fields_from_subsection(self, subsection_fields_dict: dict, subsection_text):
        for field, question in subsection_fields_dict.items():
            json = self.invoke(question, subsection_text)