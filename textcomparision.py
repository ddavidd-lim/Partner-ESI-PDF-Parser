from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine

class TextComparision:
    def  __init__(self, model_name = "sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def compare_texts(self, sentence1, sentence2):
        # Encode and compute embeddings
        with torch.no_grad():
            tokens1 = self.tokenizer(sentence1, return_tensors="pt", padding=True, truncation=True)
            tokens2 = self.tokenizer(sentence2, return_tensors="pt", padding=True, truncation=True)

            embeddings1 = self.model(**tokens1).pooler_output
            embeddings2 = self.model(**tokens2).pooler_output

        # Calculate cosine similarity (note: 1-cosine because scipy calculates distance)
        similarity = 1 - cosine(embeddings1[0].numpy(), embeddings2[0].numpy())
        return round(similarity,2)


if __name__ == "__main__":
    text_comparator = TextComparision()
    similiarity = text_comparator.compare_texts("The cat is sleeping on the sofa.", "I plan to start a new exercise regime tomorrow." )
    print(similiarity)