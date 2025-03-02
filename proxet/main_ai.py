import ollama  # Import Ollama for local LLM execution
from faiss_memory import FAISSMemory  # Import FAISS for long-term memory
from neo4j_connector import fetch_knowledge_from_neo4j  # Import Neo4j function
from app import flask

# Initialize FAISS memory for conversation history
faiss_memory = FAISSMemory()

# Specify the Ollama model to use (e.g., "mistral", "llama3", "gemma")
OLLAMA_MODEL = "mistral"

def process_input(user_input):
    """Processes user input using FAISS, Neo4j, and Ollama LLM."""

    # 1️⃣ Retrieve past conversations from FAISS (long-term memory)
    similar_conversations = faiss_memory.search_similar(user_input, top_k=2)
    retrieved_context = [text for text, _ in similar_conversations]

    # 2️⃣ Fetch related knowledge from Neo4j (graph-based reasoning)
    related_knowledge = fetch_knowledge_from_neo4j(user_input)

    # 3️⃣ Combine FAISS & Neo4j knowledge for better response
    context = "\n".join(retrieved_context + related_knowledge)

    # 4️⃣ Generate a response using Ollama
    prompt = f"Context:\n{context}\n\nUser: {user_input}\nBot:"
    response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}])

    bot_response = response["message"]["content"]  # Extract response text

    # 5️⃣ Store new messages in FAISS for long-term memory
    faiss_memory.add_message(user_input)
    faiss_memory.add_message(bot_response)

    return bot_response

# --------------- Run Chatbot ---------------- #
if __name__ == "__main__":
    print("🤖 AI Chatbot (FAISS + Ollama + Neo4j) is ready! Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = process_input(user_input)
        print(f"Bot: {response}")
