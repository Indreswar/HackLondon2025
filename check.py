# Import required libraries
import os
from neo4j_connector import Neo4jReasoning  # Import Neo4j logic
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1️⃣ Setup Neo4j Connection
NEO4J_URI = "bolt://localhost:7687"  # Change if using cloud DB
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Indresh@2006"  # Ensure this is correct

# Initialize Neo4j
db = Neo4jReasoning(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# 2️⃣ Load and Process Documents
loader = TextLoader("your_data.txt")  # Change to your file
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 3️⃣ Generate Embeddings & Store in FAISS
embedding_model = OpenAIEmbeddings()
vector_db = FAISS.from_documents(docs, embedding_model)
vector_db.save_local("faiss_index")  # Save FAISS index

# 4️⃣ Store Metadata in Neo4j
for doc in docs:
    query = """
    CREATE (d:Document {text: $text, source: $source})
    """
    db.run_query(query, {"text": doc.page_content, "source": "your_data.txt"})

print("✅ FAISS and Neo4j setup completed!")

# 5️⃣ Retrieve Relevant Information from FAISS & Neo4j
def retrieve_data(query_text):
    # Load FAISS index
    vector_db = FAISS.load_local("faiss_index", embedding_model)
    
    # Query FAISS for similar documents
    similar_docs = vector_db.similarity_search(query_text, k=3)
    
    # Query Neo4j for structured knowledge
    neo4j_query = """
    MATCH (d:Document) WHERE d.text CONTAINS $keyword RETURN d.text LIMIT 3
    """
    neo4j_results = db.run_query(neo4j_query, {"keyword": query_text})
    
    # Combine FAISS & Neo4j results
    all_docs = [doc.page_content for doc in similar_docs] + [res['d.text'] for res in neo4j_results]
    
    return "\n".join(all_docs)

# 6️⃣ Use LLM (GPT) for Answer Generation
def ask_ai(question):
    # Retrieve data from FAISS & Neo4j
    context = retrieve_data(question)

    # Initialize LLM (GPT-4, GPT-3.5, etc.)
    llm = OpenAI()

    # Create RetrievalQA Chain
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vector_db.as_retriever())

    # Generate response using retrieved knowledge
    response = qa_chain.run(context)
    return response

# 7️⃣ Query Neo4j for Social Reasoning
def ask_social_ai(person_name):
    """Ask AI about a person's social connections and groups."""
    connections = db.find_connections(person_name)
    groups = db.find_groups(person_name)

    response = f"\n🤖 AI Social Reasoning:\n"
    
    if connections:
        response += f"\nWho does {person_name} know (directly or indirectly)?\n"
        for row in connections:
            response += f"{row['From']} → {row['To']}\n"
    
    if groups:
        response += f"\nWhat groups is {person_name} a member of?\n"
        for row in groups:
            response += f"{row['Person']} → {row['Group']}\n"

    return response

# 8️⃣ Example Usage
if __name__ == "__main__":
    while True:
        print("\n1️⃣ Ask AI a general question")
        print("2️⃣ Ask AI about social connections")
        print("3️⃣ Exit")
        choice = input("\nChoose an option: ")

        if choice == "1":
            question = input("Ask something: ")
            answer = ask_ai(question)
            print("\n🤖 AI Response:\n", answer)

        elif choice == "2":
            person = input("Enter a person's name: ")
            social_info = ask_social_ai(person)
            print(social_info)

        elif choice == "3":
            print("Goodbye! 👋")
            db.close()
            break
