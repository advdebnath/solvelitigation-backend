from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

client = MongoClient("mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation?authSource=solvelitigation")
db = client["solvelitigation"]

print("⚡ Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model ready")

cursor = db.judgments.find({
    "$or": [
        {"embedding": {"$exists": False}},
        {"embedding": None}
    ]
})

total = db.judgments.count_documents({ "$or": [ { "embedding": { "$exists": False } }, { "embedding": None } ] })
print("📊 Total to process:", total)

updated = 0

for doc in cursor:
    text = doc.get("fullText", "")

    if not text or len(text) < 50:
        print("⚠️ Skipped:", doc["_id"])
        continue

    try:
        emb = model.encode(text[:2000]).tolist()

        db.judgments.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding": emb}}
        )

        updated += 1
        print("✅ Updated:", doc["_id"])

    except Exception as e:
        print("❌ Error:", doc["_id"], e)

print("🎯 TOTAL UPDATED:", updated)
