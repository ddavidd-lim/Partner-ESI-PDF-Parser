from functools import partial
import json
import os
from click import group
from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine
import torch
from typing import List, Mapping, Tuple, Union
from classes.SectionFieldsMap import SectionFieldsMap
import groupProjects
import mapping
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
        sentence1 = str(sentence1)
        sentence2 = str(sentence2)
        with torch.no_grad():
            tokens1 = self.tokenizer(sentence1, return_tensors="pt", padding=True, truncation=True)
            tokens2 = self.tokenizer(sentence2, return_tensors="pt", padding=True, truncation=True)

            embeddings1 = self.model(**tokens1).pooler_output
            embeddings2 = self.model(**tokens2).pooler_output

        # Calculate cosine similarity (note: 1-cosine because scipy calculates distance)
        similarity = 1 - cosine(embeddings1[0].numpy(), embeddings2[0].numpy())
        return round(similarity, 3) # type: ignore
    
    def compare_maps(self, ground_truth, llm_response, threshold: float) -> Mapping[str, List[Union[str, str, float]]]:
        result: Mapping[str, List[Union[str, str, float]]] = {}
        threshold /= 100
        # print(f"Ground truth: {ground_truth}\n LLM_Response: {llm_response}")
        if ground_truth == None or llm_response == None:
            return {'0': ['0', '0', 0]}
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
    
    def compare_items(self, ground_truth, llm, threshold):
        threshold /= 100
        score_listing = []
        all_fields = []
        all_fields.extend(ground_truth.keys())
        all_fields.extend(llm.keys())
        total_matching_fields = 0
        for field in all_fields:
            gt_val = ground_truth.get(field)
            llm_val = llm.get(field)
            if gt_val == None or llm_val == None:
                continue
            print(f" > gt_val: {gt_val}")
            print(f" > llm_val: {llm_val}")
            score = self.compare_texts(gt_val, llm_val)
            print(f" ! Score: {score}")
            if score > threshold:
                score_listing.append([gt_val, llm_val, score])
            total_matching_fields += 1
        total_correct = len(score_listing)
        print(f" total fields: {total_matching_fields}\n total_correct = {total_correct}")
        
        return total_correct / total_matching_fields
        
        
        
            
    


if __name__ == "__main__":
    text_comparator = TextComparison()
    section_fields_map1 = SectionFieldsMap({})
    section_fields_map2 = SectionFieldsMap({})
    llm_response = SectionFieldsMap({})

    # Add dummy data
    # for i in range(1, 11):
    #     for j in range(1,10):
    #         section_fields_map1.add_datafield(i, f"datafield{i}_{j}", f"result{i}_{j}")
    #         section_fields_map2.add_datafield(i, f"datafield{i}_{j}", f"answer{i}_{j}")
            
    # Load LLM results
    with open('data\processed\phi3_output2.json', 'r') as f:
        data = json.load(f)
        
    # print(data['1.0'].keys())
    
    # Create Section_fields_maps
    datafields_to_questions = mapping.execute()
    questions_to_datafields = {}    
    for items in sorted(datafields_to_questions.items()):
        subsection = items[0]
        questions = items[1]
        question_to_datafield_mappings = {}
        for field, question in questions.items():
            # print(f"field: {field}")
            # print(f"question: {question}")
            question_to_datafield_mappings[question] = field
        questions_to_datafields[subsection] = question_to_datafield_mappings
        
    
    for subsection, question_answer_pairs in data.items():
        for question, answer in question_answer_pairs.items():
            field = questions_to_datafields[subsection][question]
            llm_response.add_datafield(subsection, field, answer)
    
    # Get ground truth from ESA_DATA.xlsx
    results = groupProjects.execute()
    
    # print(results)
    ground_truth = results["20-301704.3"]
    gt_dict = {}
    for item in ground_truth.items():
        gt_dict[item[0]] = item[1]
    # print(f"Ground Truth: {ground_truth.items()}\n\n")
    llm_response_all = {}
    for key, val in llm_response.items():
        llm_response_all.update(val)
    # print(f"llm_response: {llm_response.items()}")
    # print(section_fields_map1.get_section_fields(1))
    # section_num = 1
    
    # # ** Section Results **
    # sfm_results = text_comparator.compare_maps(section_fields_map1.get_section_fields(section_num), section_fields_map2.get_section_fields(section_num), 0)
    # print(f"Results for section {section_num}: \n{sfm_results}")
    # correct, partially_correct, incorrect = text_comparator.retrieve_section_similarity(sfm_results)
    # print(f"Correct: {correct}\nPartially Correct: {partially_correct}\nIncorrect: {incorrect}")
    
    # # ** Document Results **
    # correct, partially_correct, incorrect, doc_results = text_comparator.retrieve_document_similarity(section_fields_map1, ground_truth, 0)
    # print(f"Results for Document: \n{doc_results}")
    # headers = ['Section Number', 'Data Field', 'Ground Truth', 'Generated Result', 'Score']
    
    # -------------------DOCUMENT RESULTS-------------------------
    
    # threshhold = 80
    # threshhold /= 100
    # print(threshhold)
    result = text_comparator.compare_items(gt_dict, llm_response_all, 90)
    print(f"Final Score: {result}")
    # 1. 0.358
    # including N/A, 472 total fields,
    # 95%: 0.3644
    # 90%: 0.4449
    # 80%: 0.572033
    # 70%: 0.8177
    # 60%: 0.949
    
    # excluding N/A, 244 total fields,
    # 95%: 0.7049
    # 90%: 0.72131
    # 80%: 0.7709
    # 70%: 0.836
    # 60%: 0.926
    
    # section = ""
    # while section != "quit":
    #     print(f"Section numbers: {list(doc_results.keys())}")
    #     section = input("> Enter a section number to view scores. Enter 'quit' to exit\n> ")
    #     if section == "exit":
    #         break
    #     elif section not in doc_results.keys():
    #         print("Invalid section number")
    #         continue
    #     else:
    #         table_data = []
    #         section_results = doc_results[int(section)]
    #         for data_field, values in section_results.items():
    #             row = [section, data_field] + values
    #             table_data.append(row)
            
    #         print(tabulate(table_data, headers=headers, floatfmt=".3f"))
    