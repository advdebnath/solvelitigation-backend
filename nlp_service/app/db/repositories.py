from datetime import datetime
from bson import ObjectId
from pymongo.errors import PyMongoError

from app.db.mongo import get_db
from app.config import settings


def update_nlp_status(
    judgment_id: str,
    status: str,
    stage: str | None = None,
    error: str | None = None,
):
    """
    Update NLP status safely for a judgment.
    Idempotent and retry-safe.
    """

    db = get_db()
    collection = db[settings.JUDGMENTS_COLLECTION]

    try:
        update = {
            "nlpStatus": status,
            "nlpUpdatedAt": datetime.utcnow(),
        }

        if stage:
            update["nlpStage"] = stage

        if error:
            update["nlpError"] = error

        result = collection.update_one(
            {"_id": ObjectId(judgment_id)},
            {"$set": update},
        )

        if result.matched_count == 0:
            raise ValueError(f"Judgment not found: {judgment_id}")

    except PyMongoError as e:
        # Let Celery retry
        raise RuntimeError(f"Mongo update failed: {str(e)}")

def update_ingestion_status(
    ingestion_id: str,
    status: str,
    error: str | None = None,
):
    """
    Update NLP status for ingestion record.
    Used in Option A architecture.
    """

    db = get_db()
    collection = db["judgmentingestions"]

    try:
        update = {
            "status": status,
            "nlpUpdatedAt": datetime.utcnow(),
        }

        if error:
            update["error"] = error

        result = collection.update_one(
            {"_id": ObjectId(ingestion_id)},
            {"$set": update},
        )

        if result.matched_count == 0:
            raise ValueError(f"Ingestion not found: {ingestion_id}")

    except PyMongoError as e:
        raise RuntimeError(f"Mongo update failed: {str(e)}")
