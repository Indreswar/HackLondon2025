import faiss  # ✅ Import FAISS
import numpy as np
from sentence_transformers import SentenceTransformer

class FAISSMemory:
    def __init__(self, embedding_model="all-MiniLM-L6-v2", dimension=384):
        """Initializes FAISS for storing and retrieving past conversations."""
        self.model = SentenceTransformer(embedding_model)
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # ✅ L2 distance search
        self.conversation_history = []  # ✅ Stores actual text inputs

    def add_message(self, message):
        """Converts a message to an embedding and adds it to FAISS index."""
        vector = self.model.encode([message])
        self.index.add(np.array(vector, dtype=np.float32))  # ✅ Fix data type
        self.conversation_history.append(message)

    def retrieve_memory(self, query, top_k=3):
        """Finds the most similar past messages to the given query."""
        if self.index.ntotal == 0:
            return []

        query_vector = self.model.encode([query])
        query_vector = np.array(query_vector, dtype=np.float32)  # ✅ Fix data type

        distances, indices = self.index.search(query_vector, top_k)
        results = [(self.conversation_history[i], distances[0][j])
                   for j, i in enumerate(indices[0]) if i != -1]

        return results
