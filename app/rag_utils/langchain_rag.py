from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Istanzia l'LLM locale
llm = Ollama(model="mistral:instruct")

# Embedding model (mistral supporta anche questo)
embedding = OllamaEmbeddings(model="mistral:instruct")


def get_qa_chain(chat_id: str):
    # Vector store con filtro sul metadato
    vectorstore = Chroma(
        collection_name="rag_chunks",
        embedding_function=embedding,
        persist_directory="./chroma_db",  # <- assicurati che sia corretto
    ).as_retriever(
        search_kwargs={"k": 4, "filter": {"chat_id": chat_id}}
    )

    # Prompt (custom se vuoi, qui base)
    prompt = PromptTemplate.from_template(
        """Sei un assistente intelligente. Rispondi basandoti SOLO sui documenti forniti.
        Documenti:
        {context}

        Domanda: {question}
        Risposta:"""
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False,
    )

    return qa_chain
