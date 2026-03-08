"""rag: chunk, embed, and retrieve context from documents."""

import os
import chromadb


MAX_CHUNK_CHARS = 500

_client = chromadb.Client()
_collection = None


def load(file_path):
    """read a file, chunk it, and store in chromadb."""
    global _collection

    with open(file_path) as f:
        text = f.read()

    chunks = _chunk(text)
    if not chunks:
        return 0

    _collection = _client.create_collection(
        name="context",
        metadata={"source": os.path.basename(file_path)},
    )

    _collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )

    return len(chunks)


def retrieve(query, k=5):
    """return top k relevant chunks for a query."""
    if _collection is None:
        return ""

    results = _collection.query(query_texts=[query], n_results=k)
    documents = results["documents"][0] if results["documents"] else []
    return "\n\n".join(documents)


def _chunk(text):
    """split text into chunks by paragraphs, respecting max size."""
    paragraphs = text.split("\n\n")
    chunks = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(para) <= MAX_CHUNK_CHARS:
            chunks.append(para)
        else:
            # split long paragraphs by sentences
            words = para.split()
            current = []
            current_len = 0
            for word in words:
                if current_len + len(word) + 1 > MAX_CHUNK_CHARS and current:
                    chunks.append(" ".join(current))
                    current = []
                    current_len = 0
                current.append(word)
                current_len += len(word) + 1
            if current:
                chunks.append(" ".join(current))

    return chunks
