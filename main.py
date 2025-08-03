from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from app.rag_utils.vectorstore import add_to_vectorstore
from app.storage import upload_file_to_r2
from app.rag_engine import extract_structured_chunks
from app.rag_utils.chunker import chunk_structured_blocks

app = FastAPI()

# CORS se serve per frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), chat_id: str = Form(...)):
    contents = await file.read()
    file_url = upload_file_to_r2(contents, file.filename, chat_id)
    return {"success": True, "file_url": file_url}

@app.post("/extract-text")
async def extract_structured(file: UploadFile = File(...)):
    file_bytes = await file.read()
    chunks = extract_structured_chunks(file_bytes, file.filename)
    return {"chunks": chunks[:3]}

@app.post("/extract-chunks")
async def extract_chunks(file: UploadFile = File(...)):
    file_bytes = await file.read()
    structured_blocks = extract_structured_chunks(file_bytes, file.filename)
    chunks = chunk_structured_blocks(structured_blocks)
    return {"num_chunks": len(chunks), "chunks": chunks[:2]}  # preview

@app.post("/upload-chunks")
async def upload_and_chunk(file: UploadFile = File(...), chat_id: str = Form(...)):
    file_bytes = await file.read()
    structured_blocks = extract_structured_chunks(file_bytes, file.filename)
    chunks = chunk_structured_blocks(structured_blocks)
    num_saved = add_to_vectorstore(chunks, chat_id)
    return {
        "message": f"{num_saved} chunk salvati per chat_id {chat_id}",
        "preview": chunks[:2]
    }