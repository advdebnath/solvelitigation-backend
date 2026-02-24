from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId

from app.tasks.judgment_task import process_judgment
from app.db.mongo import get_db

router = APIRouter()


class EnqueueRequest(BaseModel):
    judgmentId: str | None = None
    ingestionId: str | None = None


@router.post("/enqueue")
def enqueue_judgment(req: EnqueueRequest):

    db = get_db()

    ingestion_id = None

    # Case 1: ingestionId provided directly
    if req.ingestionId:
        ingestion_id = req.ingestionId

    # Case 2: judgmentId provided → resolve ingestionId
    elif req.judgmentId:
        judgment = db["judgments"].find_one(
            {"_id": ObjectId(req.judgmentId)},
            {"ingestionId": 1}
        )

        if not judgment or "ingestionId" not in judgment:
            raise HTTPException(
                status_code=400,
                detail="IngestionId not found for this judgment"
            )

        ingestion_id = str(judgment["ingestionId"])

    else:
        raise HTTPException(
            status_code=422,
            detail="Either judgmentId or ingestionId must be provided"
        )

    # Enqueue Celery task
    process_judgment.delay(ingestion_id)

    return {
        "success": True,
        "judgmentId": req.judgmentId,
        "ingestionId": ingestion_id,
        "status": "ENQUEUED"
    }
