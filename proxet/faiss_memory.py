import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

FAISS_INDEX_PATH = "faiss_index/faiss_store.index"

class FAISSMemory:
    def __init__(self, embedding_model="all-MiniLM-L6-v2", dimension=384):
        self.model = SentenceTransformer(embedding_model)
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)

        if os.path.exists(FAISS_INDEX_PATH):
            self.index = faiss.read_index(FAISS_INDEX_PATH)

    def add_message(self, message):
        vector = self.model.encode([message])
        self.index.add(np.array(vector, dtype=np.float32))
        faiss.write_index(self.index, FAISS_INDEX_PATH)

    def search_similar(self, query, top_k=3):
        if self.index.ntotal == 0:
            return []

        query_vector = self.model.encode([query])
        query_vector = np.array(query_vector, dtype=np.float32)

        distances, indices = self.index.search(query_vector, top_k)
        results = [distances[0][j] for j in indices[0] if j != -1]

        return results
