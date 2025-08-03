# app/main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.storage import upload_file_to_r2
from app.rag_engine import extract_structured_chunks
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