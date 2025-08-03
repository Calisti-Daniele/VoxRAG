import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import json


# ✅ Nuova inizializzazione consigliata
chroma_client = chromadb.HttpClient(host="localhost", port=8000)

COLLECTION_NAME = "rag_chunks"
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

def embed_texts(texts: List[str]) -> List[List[float]]:
    return EMBEDDING_MODEL.encode(texts).tolist()

def sanitize_metadata(chunk: dict, chat_id: str):
    metadata = {"chat_id": chat_id}
    for k, v in chunk.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            metadata[k] = v
        else:
            metadata[k] = json.dumps(v)
    return metadata

def add_to_vectorstore(chunks: List[Dict], chat_id: str) -> int:
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [sanitize_metadata(chunk, chat_id) for chunk in chunks]
    ids = [f"{chat_id}_{i}" for i in range(len(chunks))]
    embeddings = embed_texts(texts)

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    return len(texts)

def query_chunks_by_chat_id(chat_id: str, query: str, k: int = 4):
    results = collection.query(
        query_texts=[query],
        where={"chat_id": chat_id},
        n_results=k
    )
    return results["documents"][0]
