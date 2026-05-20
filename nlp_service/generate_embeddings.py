from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from datetime import datetime

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"

print("⚡ Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded")

db = MongoClient(MONGO_URI)["solvelitigation"]

# ============================================
# 🔥 CLEAN TEXT BUILDER (IMPROVED)
# ============================================

def build_text(j):
    headnote = j.get("headnote", "") or ""
    points = j.get("pointsOfLaw", []) or []
    case = j.get("caseNumber", "") or ""
    full = (j.get("fullText", "") or "")[:3000]   # 🔥 increased

    if isinstance(points, list):
        points_text = " ".join(points)
    else:
        points_text = str(points)

    if headnote:
        return f"{headnote} {points_text} {case}".strip()

    if points_text.strip():
        return f"{points_text} {case}".strip()

    return f"{case} {full}".strip()

# ============================================
# 🔥 RESUME-SAFE CURSOR
# ============================================

cursor = db.judgments.find({
    "$or": [
        {"embedding": {"$exists": False}},
        {"embedding": None},
        {"embedding": {"$size": 0}}
    ]
}).batch_size(50)

count = 0
skipped = 0

print("🚀 Generating embeddings...")

# ============================================
# 🔥 SAFE ITERATION (NO MEMORY OVERLOAD)
# ============================================

for j in tqdm(cursor):

    try:
        text = build_text(j)

        if not text or len(text) < 20:
            skipped += 1
            continue

        emb = model.encode(text, normalize_embeddings=True)

        if emb is None or len(emb) != 384:
            print(f"❌ Invalid embedding for {j['_id']}")
            skipped += 1
            continue

        db.judgments.update_one(
            {"_id": j["_id"]},
            {
                "$set": {
                    "embedding": emb.tolist(),
                    "embeddingCreatedAt": datetime.utcnow()  # 🔥 tracking
                }
            }
        )

        count += 1

    except Exception as e:
        print(f"❌ Error for {j['_id']}:", e)
        skipped += 1

print("===================================")
print(f"✅ TOTAL EMBEDDED: {count}")
print(f"⚠️ SKIPPED: {skipped}")
print("🚀 DONE")
