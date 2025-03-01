import ollama
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from neo4j.neo4j_connector import Neo4jReasoning  # Import Neo4j logic
from neo4j.faiss import retrieve_memory, add_to_memory  # Import FAISS logic

# Use a free embedding model (instead of OpenAI)
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialize FAISS for vector search
vector_db = FAISS.load_local("faiss_index", embedding_model)

# Initialize Neo4j Reasoning
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password_here"  # Replace with actual password
neo4j_handler = Neo4jReasoning(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# Initialize LangChain memory for short-term conversation tracking
memory = ConversationBufferMemory()

def embed_text(text):
    """Generate embeddings using a free model."""
    return embedding_model.encode(text)

def generate_response(user_id, user_message):
    """Handles AI responses using Ollama, FAISS, and Neo4j."""
    try:
        # Retrieve past chat memory
        past_memory = memory.load_memory_variables({})["chat_history"]

        # Retrieve relevant knowledge from FAISS
        retrieved_memory = retrieve_memory(user_message)

        # Retrieve structured reasoning from Neo4j
        reasoning = neo4j_handler.get_reasoning(user_message)

        # Combine memory, retrieved knowledge, and reasoning into final input
        context = f"Memory: {past_memory}\n\nRetrieved Info: {retrieved_memory}\n\nReasoning: {reasoning}"

        # Generate AI response using Ollama (local, free)
        response = ollama.chat("deepseek/deepseek-7b-chat", messages=[{"role": "user", "content": context}])
        response_text = response['message']['content']

        # Store conversation in FAISS for future retrieval
        add_to_memory(f"{user_message} -> {response_text}")

        return response_text
    
    except Exception as e:
        print(f"LangChain Error: {e}")
        return "I'm having trouble processing this request right now. Please try again."
