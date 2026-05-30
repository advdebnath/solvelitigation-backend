import torch
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"

client = MongoClient(MONGO_URI)
db = client["solvelitigation"]

model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_outcome(text):
    if not text:
        return None
    t = text.lower()
    if "allowed" in t:
        return 1
    if "dismissed" in t:
        return 0
    return None


def predict_advanced(query: str):
    if not query:
        return 50

    query_emb = model.encode(query, convert_to_tensor=True)

    cases = list(db.judgments.find().limit(200))

    scores = []

    for c in cases:
        text = c.get("fullText", "")
        outcome = extract_outcome(text)

        if not text or outcome is None:
            continue

        emb = model.encode(text[:1000], convert_to_tensor=True)

        sim = util.cos_sim(query_emb, emb).item()

        scores.append((sim, outcome))

    if not scores:
        return 50

    # 🔥 Weighted average
    total_score = 0
    total_weight = 0

    for sim, outcome in scores:
        total_score += sim * outcome
        total_weight += sim

    probability = total_score / total_weight if total_weight else 0.5

    return int(probability * 100)
