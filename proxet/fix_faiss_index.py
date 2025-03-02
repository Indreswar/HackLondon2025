import os
import pickle

faiss_index_path = "faiss_index"
faiss_metadata_file = f"{faiss_index_path}/index.pkl"

# Ensure the directory exists
os.makedirs(faiss_index_path, exist_ok=True)

# Create and save an empty FAISS metadata file
metadata = {"ids": [], "texts": []}  # ✅ Valid FAISS metadata structure

with open(faiss_metadata_file, "wb") as f:
    pickle.dump(metadata, f)

print("✅ index.pkl recreated successfully!")
