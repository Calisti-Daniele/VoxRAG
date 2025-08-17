from typing import List, Dict
from tiktoken.load import load_tiktoken_bpe
from tiktoken.core import Encoding

# Carica i mergeable ranks
mergeable_ranks = load_tiktoken_bpe("./encodings/cl100k_base.tiktoken")

# Istanzia l'encoder
enc = Encoding(
    name="cl100k_base",
    pat_str=r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""",
    mergeable_ranks=mergeable_ranks,
    special_tokens={"<|endoftext|>": 100257},
)

def count_tokens(text: str) -> int:
    return len(enc.encode(text))


def chunk_structured_blocks(blocks: List[Dict], max_tokens: int = 500) -> List[Dict]:
    chunks = []
    buffer = ""
    buffer_tokens = 0
    current_metadata = {
        "headings": [],
        "ocr_texts": [],
    }

    for block in blocks:
        block_text = block.get("text", "")
        block_type = block.get("type", "paragraph")
        level = block.get("level", None)

        if block_type == "heading":
            formatted = f"\n\n### {block_text.strip()}\n"
            current_metadata["headings"].append(block_text.strip())
        elif block_type == "image":
            ocr = block.get("ocr_text", "")
            if ocr:
                formatted = f"\n\n[🖼️ OCR Immagine]: {ocr.strip()}\n"
                current_metadata["ocr_texts"].append(ocr.strip())
            else:
                formatted = "\n\n[🖼️ Immagine senza OCR]\n"
        else:  # paragraph, text, ecc.
            formatted = f"\n{block_text.strip()}\n"

        tok_count = count_tokens(formatted)

        if buffer_tokens + tok_count > max_tokens and buffer.strip():
            chunks.append({
                "text": buffer.strip(),
                "tokens": buffer_tokens,
                "metadata": current_metadata.copy()
            })
            buffer = ""
            buffer_tokens = 0
            current_metadata = {"headings": [], "ocr_texts": []}

        buffer += formatted
        buffer_tokens += tok_count

    if buffer.strip():
        chunks.append({
            "text": buffer.strip(),
            "tokens": buffer_tokens,
            "metadata": current_metadata.copy()
        })

    return chunks
