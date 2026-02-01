from app.celery_app import celery_app
import time

@celery_app.task(name="tasks.summarize")
def summarize(text: str, max_len: int = 256):
    time.sleep(5)  # simulate heavy work
    summary = (text[:max_len] + "...") if len(text) > max_len else text
    return {"summary": summary, "length": len(summary)}
