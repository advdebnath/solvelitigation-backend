from nlp_app.env_loader import load_env
load_env()

from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from nlp_app.celery_app import celery_app
from nlp_app.tasks import summarize
import os

app = FastAPI(title="NLP Service", version="1.0")

# -------------------------------------------------------------------
# Sync endpoint
# -------------------------------------------------------------------
class EmbedReq(BaseModel):
    text: str

@app.post("/v1/embed")
def embed(req: EmbedReq):
    vec = [len(req.text) % 7 / 10.0, 0.2, 0.3]
    return {"vector": vec}

# -------------------------------------------------------------------
# Async queued endpoints
# -------------------------------------------------------------------
class SummarizeReq(BaseModel):
    text: str

@app.post("/v1/summarize/queue")
def summarize_queue(req: SummarizeReq):
    task = summarize.delay({"text": req.text})
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
# Legacy endpoint (USED BY BACKEND)
# -------------------------------------------------------------------
@app.post("/enqueue")
def enqueue(payload: dict = Body(...)):
    # Backward-compatible identifiers
    job_id = payload.get("jobId") or payload.get("judgmentId")
    lock_id = payload.get("lockId")              # 🔐 NEW (optional but expected)
    pdf_path = payload.get("pdfPath")
    text = payload.get("text")

    if not (pdf_path or text or job_id):
        raise HTTPException(status_code=400, detail="Missing payload")

    # Keep entire payload intact (important for backward compatibility)
    task = summarize.delay(payload)

    return {
        "queued": True,
        "task_id": task.id,
        "jobId": job_id,
        "lockId": lock_id,   # 🔐 echoed back for tracing/debugging
    }



# -------------------------------------------------------------------
# Health checks
# -------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "service": "nlp"}

@app.get("/healthz")
def healthz():
    return {
        "ok": True,
        "service": "nlp",
        "broker": os.getenv("REDIS_URL", ""),
    }
