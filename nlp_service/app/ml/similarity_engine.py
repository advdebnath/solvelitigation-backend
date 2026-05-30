import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"

client = MongoClient(MONGO_URI)
db = client["solvelitigation"]

# 🔥 Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# ================================
# 🔥 COSINE SIMILARITY
# ================================
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# ================================
# 🔥 FIND SIMILAR CASES
# ================================
def find_similar_cases(text, top_k=5):
    query_embedding = model.encode(text)

    judgments = list(db.judgments.find({"embedding": {"$exists": True}}).limit(500))

    scored = []

    for j in judgments:
        sim = cosine_similarity(query_embedding, j["embedding"])
        scored.append((sim, j))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [j for _, j in scored[:top_k]]


# ================================
# 🔥 DECISION ENGINE
# ================================
def decide_from_similar(text):
    similar_cases = find_similar_cases(text)

    if not similar_cases:
        return None

    # 🔥 CATEGORY
    categories = [c.get("category") for c in similar_cases if c.get("category")]
    category = max(set(categories), key=categories.count) if categories else "Unknown"

    # 🔥 ACTS
    acts = []
    for c in similar_cases:
        acts.extend(c.get("acts", []))
    acts = list(set(acts))

    # 🔥 POINTS OF LAW
    points = []
    for c in similar_cases:
        points.extend(c.get("pointsOfLaw", []))
    points = list(set(points))

    # 🔥 HEADNOTE (SMART MERGE)
    headnotes = [c.get("headnote") for c in similar_cases if c.get("headnote")]
    headnote = headnotes[0] if headnotes else None

    return {
        "confidence": similarity_score,
        "category": category,
        "acts": acts,
        "pointsOfLaw": points,
        "headnote": headnote,
    }
