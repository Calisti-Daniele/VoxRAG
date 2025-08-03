from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.rag_utils.langchain_rag import get_qa_chain
from app.rag_utils.vectorstore import add_to_vectorstore
from app.storage import upload_file_to_r2
from app.rag_engine import extract_structured_chunks
from app.rag_utils.chunker import chunk_structured_blocks

import logging

# === LOGGER BASE ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === APP FASTAPI ===
app = FastAPI(
    title="RAG Backend API",
    description="API per il caricamento file, estrazione testo, chunking e query semantiche.",
    version="1.0.0"
)

# === CORS (modifica in produzione!) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Metti domini sicuri in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ENDPOINTS ===

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), chat_id: str = Form(...)):
    contents = await file.read()
    logger.info(f"Upload file: {file.filename} per chat_id: {chat_id}")
    file_url = upload_file_to_r2(contents, file.filename, chat_id)
    return {"success": True, "file_url": file_url}


@app.post("/extract-text")
async def extract_structured(file: UploadFile = File(...)):
    file_bytes = await file.read()
    logger.info(f"Estraggo testo strutturato da: {file.filename}")
    chunks = extract_structured_chunks(file_bytes, file.filename)
    return {"chunks": chunks}


@app.post("/extract-chunks")
async def extract_chunks(file: UploadFile = File(...)):
    file_bytes = await file.read()
    logger.info(f"Estraggo + chunk da: {file.filename}")
    structured_blocks = extract_structured_chunks(file_bytes, file.filename)
    chunks = chunk_structured_blocks(structured_blocks)
    return {
        "num_chunks": len(chunks),
        "chunks": chunks[:2]  # solo preview
    }


@app.post("/upload-chunks")
async def upload_and_chunk(file: UploadFile = File(...), chat_id: str = Form(...)):
    file_bytes = await file.read()
    logger.info(f"Upload + chunk file: {file.filename} per chat_id: {chat_id}")
    structured_blocks = extract_structured_chunks(file_bytes, file.filename)
    chunks = chunk_structured_blocks(structured_blocks)
    num_saved = add_to_vectorstore(chunks, chat_id)
    return {
        "message": f"{num_saved} chunk salvati per chat_id {chat_id}",
        "preview": chunks[:2]
    }


@app.post("/rag")
async def rag(chat_id: str = Form(...), query: str = Form(...)):
    try:
        logger.info(f"RAG request - chat_id: {chat_id}, query: {query}")
        qa = get_qa_chain(chat_id)
        result = qa.run(query)
        return {"response": result}
    except Exception as e:
        logger.exception("Errore durante la generazione della risposta RAG")
        return JSONResponse(status_code=500, content={"error": str(e)})

