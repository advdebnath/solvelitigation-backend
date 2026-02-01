# FILE: nlp_service/nlp_app/main.py

from nlp_app.env_loader import load_env
load_env()  # load .env.* early

from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from nlp_app.celery_app import celery_app
import os

# Try direct task import; fallback to send_task
try:
    from app.tasks import summarize as summarize_task  # type: ignore
except Exception:
    summarize_task = None

app = FastAPI(title="NLP Service", version="1.0")

# -------------------------------------------------------------------
# Sync endpoint (example)
# -------------------------------------------------------------------
class EmbedReq(BaseModel):
    text: str

@app.post("/v1/embed")
def embed(req: EmbedReq):
    vec = [len(req.text) % 7 / 10.0, 0.2, 0.3]
    return {"vector": vec}

# -------------------------------------------------------------------
# Async queued endpoints (v1)
# -------------------------------------------------------------------
class SummarizeReq(BaseModel):
    text: str
    max_len: int = 256

@app.post("/v1/summarize/queue")
def summarize_queue(req: SummarizeReq):
    task = celery_app.send_task(
        "tasks.summarize",
        args=[req.text, req.max_len],
        queue="nlp"
    )
    return {"task_id": task.id, "status": "queued"}

@app.get("/v1/tasks/{task_id}")
def task_status(task_id: str):
    res = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "state": res.state,
        "ready": res.ready(),
        "successful": (res.successful() if res.ready() else None),
        "result": (res.result if res.ready() else None),
    }

# -------------------------------------------------------------------
# Legacy compatibility (USED BY BACKEND)
# -------------------------------------------------------------------
@app.post("/enqueue")
def enqueue(payload: dict = Body(...)):
    text = payload.get("text") or payload.get("pdfPath") or payload.get("jobId")
    if not text:
        raise HTTPException(status_code=400, detail="Missing payload")

    if summarize_task:
        r = summarize_task.delay(text)
    else:
        r = celery_app.send_task("tasks.summarize", args=[text], queue="nlp")

    return {"task_id": r.id, "status": "queued"}

# -------------------------------------------------------------------
# Task result alias (legacy)
# -------------------------------------------------------------------
@app.get("/tasks/{task_id}")
def get_result(task_id: str):
    res = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "state": res.state,
        "ready": res.ready(),
        "successful": (res.successful() if res.ready() else None),
        "result": (res.result if res.ready() else None),
    }

# -------------------------------------------------------------------
# Health checks (OPS STANDARD)
# -------------------------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "nlp"
    }

@app.get("/healthz")
def healthz():
    return {
        "ok": True,
        "service": "nlp",
        "broker": os.getenv("REDIS_URL", os.getenv("CELERY_BROKER_URL", "")),
    }

# -------------------------------------------------------------------
# Entrypoint (local dev only)
# -------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "nlp_app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )
