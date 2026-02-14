from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.celery_app import celery_app

router = APIRouter()


class EnqueueRequest(BaseModel):
    judgmentId: str


@router.post("/enqueue")
def enqueue_judgment(req: EnqueueRequest):
    try:

task = celery_app.send_task(
    "app.tasks.judgment_task.process_judgment",
    args=[req.judgmentId],
    queue="nlp",
)

        return {
            "success": True,
            "taskId": task.id,
            "judgmentId": req.judgmentId,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
