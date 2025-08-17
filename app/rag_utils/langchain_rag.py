from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Istanzia l'LLM locale
llm = Ollama(
    model="mistral:instruct",
    base_url="http://ollama:11434"  # 👈 questo è fondamentale nei container
)


# Embedding model (mistral supporta anche questo)
embedding = OllamaEmbeddings(
    model="mistral:instruct",
    base_url="http://ollama:11434"  # 👈 fix fondamentale
)



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
        """
        Sei un assistente virtuale intelligente, in grado di rispondere a qualsiasi domanda in italiano.

        L'utente può caricare dei documenti, e se disponibili, devi usarli per generare risposte accurate e pertinenti.
        Altrimenti rispondi basandonti sulle tue consocenze.

        {context}

        Domanda: {question}
        Risposta:
        """
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False,
    )

    return qa_chain
