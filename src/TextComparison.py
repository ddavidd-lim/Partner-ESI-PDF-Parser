from functools import partial
from click import group
from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine
import torch
from typing import List, Mapping, Tuple, Union
from classes.SectionFieldsMap import SectionFieldsMap
import groupProjects
from tabulate import tabulate

class TextComparison:
    def  __init__(self, model_name = "sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.similarity_scores = {}
        self.total_fields = 0
        self.section_correct = {}
        
    def compare_texts(self, sentence1: str, sentence2: str) -> float:
        # Encode and compute embeddings
        with torch.no_grad():
            tokens1 = self.tokenizer(sentence1, return_tensors="pt", padding=True, truncation=True)
            tokens2 = self.tokenizer(sentence2, return_tensors="pt", padding=True, truncation=True)

            embeddings1 = self.model(**tokens1).pooler_output
            embeddings2 = self.model(**tokens2).pooler_output

        # Calculate cosine similarity (note: 1-cosine because scipy calculates distance)
        similarity = 1 - cosine(embeddings1[0].numpy(), embeddings2[0].numpy())
        return round(similarity, 3) # type: ignore
    
    def compare_maps(self, ground_truth: Mapping[str,str], llm_response: Mapping[str,str], threshold: float) -> Mapping[str, List[Union[str, str, float]]]:
        result: Mapping[str, List[Union[str, str, float]]] = {}
        threshold /= 100
        for key,value in ground_truth.items():
            generated_token = llm_response.get(key)
            if generated_token is None:
                continue
            score = self.compare_texts(value, generated_token)

            if score > threshold:
                result[key] = [value,generated_token,score]
        self.similarity_scores = result
        return result
        
    def retrieve_section_similarity(self, similarity_scores) -> Tuple[List[str], List[str], List[str]]:
        # Record which keys are correct, partially correct, or incorrect
        correct = []
        partially_correct = []
        incorrect = []
        for datafield, score in similarity_scores.items():
            string1 = score[0]
            string2 = score[1]
            similarity = float(score[2])
            
            if similarity > 0.8:
                correct.append(datafield)
            elif similarity > 0.6:
                partially_correct.append(datafield)
            else:
                incorrect.append(datafield)
                
            # print(f"Datafield: {datafield}\nGround Truth: {string1}\nGenerated: {string2}\nSimilarity: {similarity}\n")
            
        return correct, partially_correct, incorrect
    
    def retrieve_document_similarity(self, section_fields_map1: SectionFieldsMap, section_fields_map2: SectionFieldsMap, threshold: float):
        correct = []
        partially_correct = []
        incorrect = []
        doc_results = dict()
        for section_num in section_fields_map1.fields:
            # print(f"**************\n Section {section_num} \n************** ")
            sfm_results = self.compare_maps(section_fields_map1.get_section_fields(section_num), section_fields_map2.get_section_fields(section_num), threshold)
            c, pc, ic = self.retrieve_section_similarity(sfm_results)
            correct.extend(c)
            partially_correct.extend(pc)
            incorrect.extend(ic)
            doc_results[section_num] = sfm_results
        return correct, partially_correct, incorrect, doc_results
    


if __name__ == "__main__":
    text_comparator = TextComparison()
    section_fields_map1 = SectionFieldsMap({})
    section_fields_map2 = SectionFieldsMap({})

    # Add dummy data
    for i in range(1, 11):
        for j in range(1,10):
            section_fields_map1.add_datafield(i, f"datafield{i}_{j}", f"result{i}_{j}")
            section_fields_map2.add_datafield(i, f"datafield{i}_{j}", f"answer{i}_{j}")
    
    # Get ground truth from ESA_DATA.xlsx
    # results = groupProjects.execute()
    
    # print(section_fields_map1.get_section_fields(1))
    section_num = 1
    
    # ** Section Results **
    sfm_results = text_comparator.compare_maps(section_fields_map1.get_section_fields(section_num), section_fields_map2.get_section_fields(section_num), 0)
    print(f"Results for section {section_num}: \n{sfm_results}")
    correct, partially_correct, incorrect = text_comparator.retrieve_section_similarity(sfm_results)
    print(f"Correct: {correct}\nPartially Correct: {partially_correct}\nIncorrect: {incorrect}")
    
    # ** Document Results **
    correct, partially_correct, incorrect, doc_results = text_comparator.retrieve_document_similarity(section_fields_map1, section_fields_map2, 0)
    # print(f"Results for Document: \n{doc_results}")
    headers = ['Section Number', 'Data Field', 'Ground Truth', 'Generated Result', 'Score']
    
    section = ""
    while section != "quit":
        print(f"Section numbers: {list(doc_results.keys())}")
        section = input("> Enter a section number to view scores. Enter 'quit' to exit\n> ")
        if section == "exit":
            break
        elif int(section) not in doc_results.keys():
            print("Invalid section number")
            continue
        else:
            table_data = []
            section_results = doc_results[int(section)]
            for data_field, values in section_results.items():
                row = [section, data_field] + values
                table_data.append(row)
            
            print(tabulate(table_data, headers=headers, floatfmt=".3f"))
    