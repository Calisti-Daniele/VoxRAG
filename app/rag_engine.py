import os
import io
import logging
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from docx import Document
from typing import List, Dict
from app.logging_config import setup_logger

logger = setup_logger()

def extract_structured_chunks(file_bytes: bytes, filename: str, enable_ocr: bool = True) -> List[Dict]:
    ext = os.path.splitext(filename)[1].lower()
    logger.debug(f"Estensione rilevata: {ext}")

    if ext == ".pdf":
        return extract_from_pdf(file_bytes, enable_ocr)
    elif ext == ".docx":
        return extract_from_docx(file_bytes)
    elif ext == ".txt":
        return extract_from_txt(file_bytes)
    else:
        raise ValueError(f"❌ Estensione non supportata: {ext}")


def extract_from_pdf(file_bytes: bytes, enable_ocr: bool = True) -> List[Dict]:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    chunks = []
    logger.debug(f"Documento PDF aperto con {len(doc)} pagine.")

    for page_index, page in enumerate(doc):
        logger.debug(f"Processo pagina {page_index + 1}/{len(doc)}")

        # === Testo ===
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block["type"] == 0:
                paragraph = ""
                max_font_size = 0
                for line in block["lines"]:
                    for span in line["spans"]:
                        paragraph += span["text"] + " "
                        max_font_size = max(max_font_size, span.get("size", 0))

                if paragraph.strip():
                    chunk_type = "heading" if max_font_size > 15 else "paragraph"
                    chunks.append({
                        "type": chunk_type,
                        "text": paragraph.strip(),
                        "level": 1 if chunk_type == "heading" else None
                    })

        # === Immagini + OCR ===
        if enable_ocr:
            image_list = page.get_images(full=True)
            logger.debug(f"Trovate {len(image_list)} immagini nella pagina {page_index + 1}.")

            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    logger.debug(f"Estrazione immagine con xref={xref}")
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    try:
                        image = image.convert("L")  # scala di grigi
                        image = image.point(lambda x: 0 if x < 128 else 255, '1')  # binarizzazione
                        ocr_text = pytesseract.image_to_string(image, lang="eng")
                    except pytesseract.TesseractNotFoundError:
                        logger.warning("❗ Tesseract non trovato: OCR saltato per questa immagine.")
                        ocr_text = None

                    chunks.append({
                        "type": "image",
                        "text": "🖼️ Immagine nel documento",
                        "caption": None,
                        "ocr_text": ocr_text.strip() or None
                    })
                    logger.debug(f"OCR estratto: {ocr_text.strip()[:50]}...")

                except Exception as e:
                    logger.exception(f"Errore durante l'elaborazione dell'immagine {img_index} nella pagina {page_index + 1}")

    return chunks


def extract_from_docx(file_bytes: bytes) -> List[Dict]:
    doc = Document(io.BytesIO(file_bytes))
    chunks = []
    logger.debug("Documento DOCX caricato.")

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        style = para.style.name.lower()
        if "heading" in style:
            try:
                level = int(style.replace("heading", "").strip())
            except:
                level = 1
            chunks.append({"type": "heading", "text": text, "level": level})
            logger.debug(f"Heading trovato: {text}")
        else:
            chunks.append({"type": "paragraph", "text": text, "level": None})
            logger.debug(f"Paragrafo trovato: {text[:50]}...")

    return chunks


def extract_from_txt(file_bytes: bytes) -> List[Dict]:
    text = file_bytes.decode("utf-8", errors="ignore")
    lines = text.splitlines()
    chunks = []

    for line in lines:
        if line.strip():
            chunks.append({"type": "paragraph", "text": line.strip(), "level": None})
            logger.debug(f"Linea di testo trovata: {line.strip()}")

    return chunks
