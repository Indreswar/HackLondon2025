import ollama
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from faiss.retrieve_memory import retrieve_memory
from faiss.add_to_memory import add_to_memory
from neo4j.neo4j_reasoning import Neo4jReasoning  # Neo4j reasoning logic

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.load_local("faiss_index", embedding_model)

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password_here"  
neo4j_handler = Neo4jReasoning(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

memory = ConversationBufferMemory()

def generate_response(user_id, user_message):
    """Handles AI responses using Ollama, FAISS, and Neo4j."""
    try:
        past_memory = memory.load_memory_variables({})["chat_history"]
        retrieved_memory = retrieve_memory(user_message)
        reasoning = neo4j_handler.get_reasoning(user_message)

        context = f"Memory: {past_memory}\n\nRetrieved Info: {retrieved_memory}\n\nReasoning: {reasoning}"

        response = ollama.chat("deepseek/deepseek-7b-chat", messages=[{"role": "user", "content": context}])
        response_text = response['message']['content']

        add_to_memory(f"{user_message} -> {response_text}")

        return response_text
    
    except Exception as e:
        print(f"LangChain Error: {e}")
        return "I'm having trouble processing this request right now. Please try again."
