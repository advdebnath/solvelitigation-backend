from sentence_transformers import SentenceTransformer
import re

# =========================================
# 🔥 GLOBAL MODEL (LOAD ON IMPORT)
# =========================================
print("🚀 Loading embedding model (GLOBAL)...")

try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Embedding model loaded (GLOBAL)")
except Exception as e:
    print("❌ MODEL LOAD ERROR:", e)
    model = None


# =========================================
# 🔥 TEXT CLEANING
# =========================================
def clean_text(text: str):
    if not text:
        return ""

    text = text.lower()

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # remove standalone numbers
    text = re.sub(r"\b\d+\b", "", text)

    return text.strip()


# =========================================
# 🔥 EMBEDDING GENERATION
# =========================================
def generate_embedding(text: str):
    try:
        if not text or model is None:
            return None

        text = clean_text(text)

        # 🔥 HARD LIMIT (IMPORTANT)
        text = text[:2000]

        embedding = model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    except Exception as e:
        print("❌ EMBEDDING ERROR:", e)
        return None


# =========================================
# 🔥 BATCH EMBEDDING
# =========================================
def generate_embeddings_batch(texts):
    try:
        if not texts or model is None:
            return []

        cleaned = [clean_text(t)[:2000] for t in texts]

        embeddings = model.encode(
            cleaned,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    except Exception as e:
        print("❌ BATCH EMBEDDING ERROR:", e)
        return []
