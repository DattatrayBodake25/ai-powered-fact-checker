import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class FactRetriever:
    def __init__(self, index_path='data/faiss_index.idx', meta_path='data/metadata.pkl', model_name='all-MiniLM-L6-v2'):
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'rb') as f:
            self.df = pickle.load(f)
        self.model = SentenceTransformer(model_name)

    def retrieve(self, claim, k=3):
        query_vector = self.model.encode([claim])
        distances, indices = self.index.search(query_vector, k)
        results = [self.df.iloc[i]['text'] for i in indices[0]]
        return results

if __name__ == "__main__":
    retriever = FactRetriever()
    claim = "India conducted Operation Sindoor as a counter-terror mission in Jammu & Kashmir."
    results = retriever.retrieve(claim)
    print("Top-K Retrieved Facts:")
    for r in results:
        print("-", r)