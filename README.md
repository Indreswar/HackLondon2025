# **FAISS + Neo4j AI Chatbot**
🚀 A chatbot using **FAISS for memory storage**, **Neo4j for reasoning**, and **Ollama for AI-generated responses**.

---

## **📌 Features**
✔️ **Retrieves past messages** using FAISS (Vector Database).  
✔️ **Uses Neo4j for structured reasoning and knowledge graphs.**  
✔️ **AI-generated responses** using the Ollama model.  
✔️ **Web-based frontend** powered by Flask.  

---
![System Design](agi_system_design.png)
---

## **📂 Project Structure**
```
proxet/
│── app.py               # Flask API server
│── langlogic.py         # AI logic, FAISS memory, and Neo4j integration
│── faiss_index/         # Stores FAISS index files (index.faiss, index.pkl)
│── faiss_utils/         # FAISS helper functions
│── graph_db/            # Neo4j reasoning module (renamed from neo4j/)
│── templates/
│   ├── index.html       # Chatbot frontend UI
│── static/
│   ├── chatbot.js       # Frontend logic (AJAX for sending messages)
│   ├── style.css        # Basic CSS styling
│── requirements.txt     # List of required Python dependencies
│── README.md            # Project documentation (this file)
```

---

## **⚙️ Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Neo4j Database**
- **Start Neo4j:**
  ```bash
  neo4j console
  ```
- **Set up credentials in your environment:**
  ```bash
  export NEO4J_URI="bolt://localhost:7687"
  export NEO4J_USER="neo4j"
  export NEO4J_PASSWORD="your_password_here"
  ```

### **5️⃣ Fix FAISS Index (If Needed)**
If you get an error about `index.pkl`, **run this to regenerate it**:
```bash
python fix_faiss_index.py
```

---

## **🚀 Running the Chatbot**
### **Start the Flask Server**
```bash
python app.py
```
- The server runs at: **http://127.0.0.1:5000/**

### **Test the Chatbot API**
```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"user_id": "123", "message": "Hello"}'
```

---

## **🌐 Using the Web Interface**
1. Open a browser and go to:  
   👉 **http://127.0.0.1:5000/**
2. Type a message and press "Send".
3. The chatbot will respond!

---

## **🔍 Troubleshooting**
### **1️⃣ FAISS Index Errors (`index.pkl` missing)**
- **Fix:** Run:
  ```bash
  python fix_faiss_index.py
  ```

### **2️⃣ Import Errors for `neo4j.GraphDatabase`**
- **Fix:** Rename `neo4j/` to `graph_db/` and update imports:
  ```python
  from graph_db.neo4j_reasoning import Neo4jReasoning
  ```

### **3️⃣ Missing Dependencies**
- **Fix:** Run:
  ```bash
  pip install -r requirements.txt
  ```

---

## **🛠 Future Improvements**
✅ **Implement authentication for chat history**  
✅ **Improve response generation with fine-tuned models**  
✅ **Optimize FAISS indexing for larger datasets**  
✅ **Deploy as a cloud-based chatbot**  

---

## **🚀 Happy Coding!** 🎉

---