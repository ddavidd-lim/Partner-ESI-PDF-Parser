from functools import partial
from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine
import torch
from typing import Mapping
from classes.SectionFieldsMap import SectionFieldsMap

class TextComparison:
    def  __init__(self, model_name = "sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

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
    
    def compare_maps(self, ground_truth: Mapping[str,str], llm_response: Mapping[str,str], threshold: float) -> Mapping[str, list[str]]:
        result = {}
        threshold /= 100
        for key,value in ground_truth.items():
            generated_token = llm_response.get(key)
            if generated_token is None:
                continue
            score = self.compare_texts(value, generated_token)

            if score > threshold:
                result[key] = [value,generated_token,score]
        
        return result


if __name__ == "__main__":
    text_comparator = TextComparison()
    m1 = {"field1":"cat is in the bag","field2":"good morning","field3":"pretty"}
    m2 = {"field1":"dog is in the bag","field2":"good afternoon","field3": "beautiful"}
    section_fields_map1 = SectionFieldsMap({})
    section_fields_map2 = SectionFieldsMap({})

    # Add dummy data
    for i in range(1, 11):
        section_fields_map1.add_datafield(1, f"datafield_{i}", f"result_{i}")
        section_fields_map2.add_datafield(1, f"datafield_{i}", f"answer_{i}")
    
    # print(section_fields_map1.get_section_fields(1))
    section_num = 1
    sfm_results = text_comparator.compare_maps(section_fields_map1.get_section_fields(section_num), section_fields_map2.get_section_fields(section_num), 0)
    print(f"Results for section {section_num}: \n{sfm_results}")
    correct = []
    partially_correct = []
    incorrect = []
    
    for datafield, result in sfm_results.items():
        string1 = result[0]
        string2 = result[1]
        similarity = float(result[2])
        
        if similarity > 0.8:
            correct.append(datafield)
        elif similarity > 0.6:
            partially_correct.append(datafield)
        else:
            incorrect.append(datafield)
            
        print(f"Datafield: {datafield}\nGround Truth: {result[0]}\nGenerated: {result[1]}\nSimilarity: {result[2]}\n")
    
    print(f"Correct: {correct}\nPartially Correct: {partially_correct}\nIncorrect: {incorrect}")
    # m_result = text_comparator.compare_maps(m1,m2,80)
    # print(m_result)