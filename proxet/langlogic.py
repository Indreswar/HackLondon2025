import sys
import os
import ollama
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory

# ✅ Ensure Python can find the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# ✅ Import FAISS & Neo4j logic
try:
    from faiss_utils.retrieve_memory import FAISSMemory
    from faiss_utils import add_to_memory
    from graph_db.neo4j_reasoning import Neo4jReasoning  # ✅ Updated import
    print("✅ Successfully imported FAISS and Neo4j modules!")
except ModuleNotFoundError as e:
    print(f"❌ ERROR: Python cannot find FAISS or Neo4j modules! {e}")
    exit(1)

# ✅ Initialize Sentence Transformer for embeddings
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ✅ Define FAISS index path
faiss_index_path = "faiss_index"
faiss_index_file = f"{faiss_index_path}/index.faiss"
faiss_metadata_file = f"{faiss_index_path}/index.pkl"  # LangChain metadata file

# ✅ Check if FAISS index files exist & load them
if os.path.exists(faiss_index_file) and os.path.exists(faiss_metadata_file):
    vector_db = FAISS.load_local(faiss_index_path, embedding_model, allow_dangerous_deserialization=True)
    print("✅ FAISS index loaded successfully!")
else:
    print("⚠️ FAISS index files missing! Creating a new index...")

    # Define FAISS index dimensions
    dimension = 384  # Adjust based on your model
    os.makedirs(faiss_index_path, exist_ok=True)

    # Create a new FAISS index
    index = faiss.IndexFlatL2(dimension)
    faiss.write_index(index, faiss_index_file)  # Save FAISS index file

    # Create and save an empty `index.pkl` for LangChain
    with open(faiss_metadata_file, "wb") as f:
        pickle.dump({}, f)

    vector_db = None  # FAISS is empty until data is added
    print("✅ New FAISS index and metadata created!")

# ✅ Initialize FAISS Memory Handler
faiss_memory = FAISSMemory()

# ✅ Load Neo4j Credentials (Use environment variables)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "your_password_here")
neo4j_handler = Neo4jReasoning(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# ✅ Initialize LangChain Memory
memory = ConversationBufferMemory()

def generate_response(user_id, user_message):
    """Handles AI responses using Ollama, FAISS, and Neo4j."""
    try:
        # Retrieve past conversation memory
        past_memory = memory.load_memory_variables({}).get("chat_history", "")

        # Retrieve similar messages using FAISS
        retrieved_memory = faiss_memory.retrieve_memory(user_message)
        print(f"🔍 FAISS Retrieved: {retrieved_memory}")

        # Get reasoning from Neo4j
        reasoning = neo4j_handler.get_reasoning(user_message)

        # Prepare conversation context
        context = f"Memory: {past_memory}\n\nRetrieved Info: {retrieved_memory}\n\nReasoning: {reasoning}"
        
        # Generate response using Ollama AI model
        response = ollama.chat("deepseek/deepseek-7b-chat", messages=[{"role": "user", "content": context}])
        response_text = response['message']['content']

        # Store the new conversation in FAISS memory
        print(f"📝 Storing in FAISS: {user_message} -> {response_text}")
        faiss_memory.add_message(user_message)
        faiss_memory.add_message(response_text)

        return response_text

    except Exception as e:
        print(f"❌ LangLogic Error: {e}")
        return "⚠️ I'm having trouble processing this request right now. Please try again."
