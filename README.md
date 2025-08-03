# VoxRAG

**VoxRAG** is a modern and modular RAG (Retrieval-Augmented Generation) platform designed to enable multi-document conversational AI. Users can upload files, extract and index content, and interact via a chatbot capable of answering questions based solely on uploaded knowledge.

---

## 🚀 Features

- 📁 Upload documents (PDF, DOCX, TXT)
- 🧩 Automatic chunking and embedding with Sentence Transformers
- 🧠 Query with LangChain + Ollama (local LLMs like Mistral)
- 🧠 Vector search with ChromaDB
- 📦 Containerized with Docker and Docker Compose
- 🌐 FastAPI backend with modular routes

---

## 🧠 Technologies Used

- **LangChain**: for building the RAG pipeline and question-answering chain
- **Ollama**: to run local large language models like `mistral:instruct`
- **ChromaDB**: local vector store for semantic search
- **HuggingFace Sentence Transformers**: for embedding document chunks (`all-MiniLM-L6-v2`)
- **FastAPI**: for building the backend API endpoints
- **Docker + Docker Compose**: for full development and deployment environments

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/voxrag.git
cd voxrag

# Build and run with Docker Compose
docker compose up --build
```

The backend will be available at `http://localhost:8000`, and the Ollama API at `http://localhost:11434`.

---

## 📁 Project Structure

```
.
├── app/
│   ├── rag_utils/           # Chunking, embeddings, vectorstore logic
│   ├── routes/              # FastAPI endpoints (upload, extract, query...)
│   └── ...                  # Other internal logic
├── start.sh                 # Entrypoint to run the FastAPI app
├── main.py                  # FastAPI application entrypoint
├── Dockerfile               # Backend Docker setup
├── docker-compose.yml       # All services: backend, chroma, ollama
└── requirements.txt         # Python dependencies
```

---

## 💬 Example Usage

1. Upload a document via `/upload`
2. Extract chunks via `/extract-chunks`
3. Index content into ChromaDB via `/add-to-vectorstore`
4. Ask questions via `/ask`

---
