# faiss_index.py
from sentence_transformers import SentenceTransformer # type: ignore
import faiss # type: ignore
import numpy as np
import json

MODEL_NAME = "all-mpnet-base-v2"
INDEX_FILE = "plag_index.faiss"
METADATA_FILE = "plag_metadata.json"
CORPUS_FILE = "corpus.txt"  # create this file with sample texts, one per line

def build_index():
    model = SentenceTransformer(MODEL_NAME)
    texts = []
    with open(CORPUS_FILE, "r", encoding="utf8") as f:
        for line in f:
            t = line.strip()
            if t:
                texts.append(t)

    emb = model.encode(texts, convert_to_numpy=True, show_progress_bar=True).astype("float32")
    faiss.normalize_L2(emb)

    dim = emb.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(emb)
    faiss.write_index(index, INDEX_FILE)

    # save metadata
    with open(METADATA_FILE, "w", encoding="utf8") as mf:
        json.dump(texts, mf, ensure_ascii=False, indent=2)

    print(f"Built index {INDEX_FILE} with {len(texts)} entries.")

if __name__ == "__main__":
    build_index()
