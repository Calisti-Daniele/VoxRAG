# VectorMind

**Chat with your documents. Locally. No limits.**

VectorMind is an open-source Retrieval-Augmented Generation (RAG) platform that lets users upload personal documents (PDF, CSV, DOCX) and interact with them via a conversational AI. Each session is persistent, context-aware, and private.

## ✨ Features

- ✅ Upload your own documents (PDF, CSV, DOCX)
- ✅ Embedding generation and Qdrant vector search
- ✅ Chat with context using open-source LLMs (e.g. Mistral)
- ✅ Modern frontend with React + Vite
- ✅ Authentication via email/password or Google
- ✅ File storage via Backblaze B2
- ✅ Each user can have multiple persistent chats

## 🧠 AI Model

We're currently using [Mistral 7B Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) locally via [Ollama](https://ollama.com/). Easily swappable with OpenAI, Claude, or any LLM API.

## 📦 Tech Stack

- **Backend**: FastAPI + Qdrant + Langchain
- **Frontend**: React + Vite + Tailwind
- **Storage**: Backblaze B2
- **Auth**: Supabase or Firebase Auth (optional)

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/yourname/vectormind.git
   cd vectormind
   ```

2. Run Qdrant locally:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

3. Start Ollama:
   ```bash
   ollama run mistral
   ```

4. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

5. Install frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📄 License

MIT — Open Source and free for everyone.
