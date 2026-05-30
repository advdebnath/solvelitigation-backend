# ✅ IMPORT TASK
from app.tasks.judgment_task import process_judgment
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


# =========================================
# 🔥 REQUEST MODEL
# =========================================
class IngestionRequest(BaseModel):
    ingestionId: str


# =========================================
# 🔥 ENQUEUE ROUTE
# =========================================
@router.post("/enqueue")
async def enqueue_task(req: IngestionRequest):
    try:
        ingestion_id = req.ingestionId

        # 🔥 VALIDATION
        if not ingestion_id:
            raise HTTPException(status_code=400, detail="Missing ingestionId")

        if not ObjectId.is_valid(ingestion_id):
            raise HTTPException(status_code=400, detail="Invalid ingestionId")

        print(f"📨 ENQUEUE RECEIVED: {ingestion_id}")

        # =========================================
        # 🔥 SEND TASK TO CORRECT QUEUE (CRITICAL)
        # =========================================
        task = process_judgment.apply_async(
            args=[ingestion_id],
            queue="celery",  # must match worker queue
            retry=False,  # prevent duplicate enqueue issues
        )

        print(f"🚀 TASK SENT TO CELERY: {task.id}")

        return {
            "success": True,
            "status": "ENQUEUED",
            "ingestionId": ingestion_id,
            "taskId": str(task.id),
        }

    except HTTPException:
        raise

    except Exception as e:
        print("❌ ENQUEUE ERROR:", str(e))

        raise HTTPException(status_code=500, detail="Failed to enqueue task")
