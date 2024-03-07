import openai
import numpy as np
import os

from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine

# USING OPENAI

# Replace "your_api_key_here" with your actual OpenAI API key
# openai.api_key = os.getenv("openai-key")

# def get_embedding(sentence):
#     response = openai.Embedding.create(
#         input=sentence,
#         engine="text-similarity-davinci-002",  # Choose an appropriate embedding engine
#     )
#     embedding = response['data'][0]['embedding']
#     return np.array(embedding)

# def cosine_similarity(vec_a, vec_b):
#     return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))

# # Example sentences
# sentence_1 = "I have a dream."
# sentence_2 = "My dream is to have a house."

# # Get embeddings
# embedding_1 = get_embedding(sentence_1)
# embedding_2 = get_embedding(sentence_2)

# # Calculate and print cosine similarity
# similarity = cosine_similarity(embedding_1, embedding_2)
# print(f"Cosine Similarity: {similarity}")



# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Sentences to compare
# High similiarity 
# sentence1 = "He is reading a book in the library."
# sentence2 = "She is studying literature at the library."

# Moderate similiarity
# sentence1 = "He is reading a book in the library."
# sentence2 = "She is studying literature at the library."

# Low similiarity
sentence1 = "The cat is sleeping on the sofa."
sentence2 = "I plan to start a new exercise regime tomorrow."


# Encode and compute embeddings
with torch.no_grad():
    tokens1 = tokenizer(sentence1, return_tensors="pt", padding=True, truncation=True)
    tokens2 = tokenizer(sentence2, return_tensors="pt", padding=True, truncation=True)

    embeddings1 = model(**tokens1).pooler_output
    embeddings2 = model(**tokens2).pooler_output

# Calculate cosine similarity (note: 1-cosine because scipy calculates distance)
similarity = 1 - cosine(embeddings1[0].numpy(), embeddings2[0].numpy())

print(f"Similarity: {similarity}")





# if __name__ == "__main__":
#     print(os.getenv("openai-key"))