from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["solvelitigation"]

REPLACEMENTS = {
    "judgmen": "judgment",
    "governmen": "government",
    "appellan": "appellant",
    "responden": "respondent",
    "ribunal": "tribunal",
}

query = {
    "fullText": {
        "$regex": "judgmen|governmen|appellan|responden|ribunal",
        "$options": "i"
    }
}

updated_docs = 0
total_replacements = 0

for doc in db.judgments.find(
    query,
    {
        "_id": 1,
        "fullText": 1,
        "cleanText": 1
    }
):

    full_text = doc.get("fullText") or ""
    clean_text = doc.get("cleanText") or ""

    replacement_count = 0

    for old, new in REPLACEMENTS.items():

        replacement_count += full_text.lower().count(old)

        full_text = full_text.replace(old, new)
        clean_text = clean_text.replace(old, new)

    if replacement_count == 0:
        continue

    db.judgments.update_one(
        {"_id": doc["_id"]},
        {
            "$set": {
                "fullText": full_text,
                "cleanText": clean_text,
                "ocrCleanupAt": datetime.utcnow()
            }
        }
    )

    updated_docs += 1
    total_replacements += replacement_count

print("=" * 60)
print("UPDATED DOCS:", updated_docs)
print("TOTAL REPLACEMENTS:", total_replacements)
print("=" * 60)
