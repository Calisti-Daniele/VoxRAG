from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document

from typing import List, Dict
import json

# === Config
COLLECTION_NAME = "rag_chunks"
CHROMA_PERSIST_DIRECTORY = "./chroma_db"

# === EMBEDDING MODEL (dim: 4096, usa Ollama Mistral)
embedding = OllamaEmbeddings(model="mistral:instruct")

# === INIT CHROMA + COLLECTION
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embedding,
    persist_directory=CHROMA_PERSIST_DIRECTORY
)

def sanitize_metadata(chunk: dict, chat_id: str) -> dict:
    metadata = {"chat_id": chat_id}
    for k, v in chunk.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            metadata[k] = v
        else:
            metadata[k] = json.dumps(v)
    return metadata

def add_to_vectorstore(chunks: List[Dict], chat_id: str) -> int:
    docs: List[Document] = []

    for i, chunk in enumerate(chunks):
        text = chunk.get("text", "")
        metadata = sanitize_metadata(chunk, chat_id)
        doc = Document(page_content=text, metadata=metadata)
        docs.append(doc)

    vectorstore.add_documents(docs)
    vectorstore.persist()
    return len(docs)

def query_chunks_by_chat_id(chat_id: str, query: str, k: int = 4) -> List[str]:
    retriever = vectorstore.as_retriever(search_kwargs={
        "k": k,
        "filter": {"chat_id": chat_id}
    })

    docs = retriever.invoke(query)
    return [doc.page_content for doc in docs]
