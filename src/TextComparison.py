from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine
import torch
from typing import Mapping

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
        return round(similarity,3)
    
    def compare_maps(self, ground_truth: Mapping[str,str], llm_response: Mapping[str,str], threshold: int) -> Mapping[str,[str]]:
        result = {}
        threshold /= 100
        for key,value in ground_truth.items():
            generated_token = llm_response.get(key)
            score = self.compare_texts(value,generated_token)

            if score < threshold:
                result[key] = [value,generated_token,score]
        
        return result


if __name__ == "__main__":
    text_comparator = TextComparison()
    m1 = {"field1":"cat is in the bag","field2":"good morning","field3":"pretty"}
    m2 = {"field1":"dog is in the bag","field2":"good afternoon","field3": "beautiful"}
    m_result = text_comparator.compare_maps(m1,m2,90)