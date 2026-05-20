# (import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"

# ================= DB =================
def get_db():
    return MongoClient(MONGO_URI)["solvelitigation"]

# ================= MODEL =================
_model = None

def get_model():
    global _model
    if _model is None:
        print("⚡ Loading semantic model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Model ready")
    return _model

# ================= SIMILARITY =================
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    if len(a) == 0 or len(b) == 0:
        return 0

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

# ================= SEARCH =================
def semantic_search(query, limit=5):
    db = get_db()
    model = get_model()

    query_emb = model.encode(query).tolist()

    results = []

    for doc in db.judgments.find({"embedding": {"$exists": True}}):
        score = cosine_similarity(query_emb, doc.get("embedding", []))

        results.append({
            "score": float(score),
            "case": doc.get("caseNumber"),
            "headnote": doc.get("headnote"),
            "category": doc.get("category"),
            "points": doc.get("pointsOfLaw", [])
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:limit]

# ================= ANSWER BUILDER =================
def generate_answer(query):
    results = semantic_search(query, limit=3)

    if not results:
        return "No relevant judgments found."

    answer = "🔎 Based on similar cases:\n\n"

    for r in results:
        answer += f"- {r['headnote']} (Score: {round(r['score'],2)})\n"

    return answer

# ================= ARGUMENT BUILDER =================
def build_argument(query):
    results = semantic_search(query, limit=5)

    arguments = []

    for r in results:
        arguments.append({
            "point": r["headnote"],
            "support": r["points"]
        })

    return arguments
