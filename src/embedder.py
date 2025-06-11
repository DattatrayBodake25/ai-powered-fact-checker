from src.utils import setup_logging
import os
import pickle
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from typing import List
from utils import setup_logger

logger = setup_logging()

class FactEmbedder:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()

    def load_facts(self, filepath: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(filepath)
            if 'text' not in df.columns:
                raise ValueError("CSV must contain 'text' column")
            return df
        except Exception as e:
            logger.error(f"Error loading facts: {e}")
            raise

    def embed_facts(self, facts: List[str]) -> np.ndarray:
        return self.model.encode(
            facts, 
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def save_embeddings(self, 
                       vectors: np.ndarray, 
                       df: pd.DataFrame, 
                       index_path: str, 
                       meta_path: str) -> None:
        try:
            os.makedirs(os.path.dirname(index_path), exist_ok=True)
            
            index = faiss.IndexFlatIP(self.dim)
            faiss.normalize_L2(vectors)
            index.add(vectors)
            
            faiss.write_index(index, index_path)
            with open(meta_path, 'wb') as f:
                pickle.dump(df, f)
                
            logger.info(f"Saved index with {len(df)} entries")
        except Exception as e:
            logger.error(f"Error saving embeddings: {e}")
            raise

    def build_index(self, csv_path: str, 
                   index_path: str = 'index/faiss.index', 
                   meta_path: str = 'index/metadata.pkl') -> None:
        try:
            df = self.load_facts(csv_path)
            embeddings = self.embed_facts(df['text'].tolist())
            self.save_embeddings(embeddings, df, index_path, meta_path)
        except Exception as e:
            logger.error(f"Index building failed: {e}")
            raise

if __name__ == "__main__":
    embedder = FactEmbedder()
    embedder.build_index("data/verified_facts.csv")