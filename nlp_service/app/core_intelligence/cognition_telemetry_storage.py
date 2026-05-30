# =========================================================
# 🔥 COGNITION TELEMETRY STORAGE
# =========================================================

from app.models.cognition_telemetry_model import build_telemetry_document
from pymongo import MongoClient

# =========================================================
# 🔥 MONGO CONNECTION
# =========================================================

client = MongoClient("mongodb://127.0.0.1:27017")

db = client["solvelitigation"]

telemetry_collection = db["cognition_telemetry"]

# =========================================================
# 🔥 STORE TELEMETRY
# =========================================================


def store_telemetry(agent_name, event_type, payload=None):

    try:

        document = build_telemetry_document(
            agent_name=agent_name, event_type=event_type, payload=payload
        )

        result = telemetry_collection.insert_one(document)

        return {"success": True, "inserted_id": str(result.inserted_id)}

    except Exception as e:

        print("❌ TELEMETRY STORAGE ERROR:")

        print(str(e))

        return {"success": False, "error": str(e)}


# =========================================================
# 🔥 FETCH TELEMETRY
# =========================================================


def fetch_recent_telemetry(limit=10):

    try:

        documents = list(
            telemetry_collection.find().sort("created_at", -1).limit(limit)
        )

        for doc in documents:

            doc["_id"] = str(doc["_id"])

        return documents

    except Exception as e:

        print("❌ TELEMETRY FETCH ERROR:")

        print(str(e))

        return []
