import os
import requests
from nlp_app.celery_app import celery_app

BACKEND_CALLBACK_URL = (
    os.getenv("BACKEND_CALLBACK_URL")
    or "http://127.0.0.1:4000/api/nlp/callback"
)

@celery_app.task(bind=True, max_retries=3)
def summarize(self, payload: dict):
    judgment_id = payload.get("judgmentId")
    lock_id = payload.get("lockId")

    if not lock_id:
        # Cannot proceed without lockId
        return {"ok": False, "error": "lockId missing"}

    try:
        # --------------------------------------------------
        # CALLBACK: MARK AS RUNNING
        # --------------------------------------------------
        requests.post(
            BACKEND_CALLBACK_URL,
            json={
                "lockId": lock_id,
                "status": "RUNNING",
            },
            timeout=5,
        )

        # --------------------------------------------------
        # NLP / SUMMARIZATION LOGIC (PLACEHOLDER)
        # --------------------------------------------------
        # TODO: Replace with real PDF/text processing
        result = {
            "pointsOfLaw": ["IPC 302", "Circumstantial Evidence"],
            "acts": ["Indian Penal Code"],
        }

        # --------------------------------------------------
        # CALLBACK: SUCCESS
        # --------------------------------------------------
        requests.post(
            BACKEND_CALLBACK_URL,
            json={
                "lockId": lock_id,
                "status": "COMPLETED",
                "pointsOfLaw": result["pointsOfLaw"],
                "acts": result["acts"],
            },
            timeout=10,
        )

        return {"ok": True}

    except Exception as exc:
        # --------------------------------------------------
        # CALLBACK: FAILURE
        # --------------------------------------------------
        try:
            requests.post(
                BACKEND_CALLBACK_URL,
                json={
                    "lockId": lock_id,
                    "status": "FAILED",
                    "error": str(exc),
                },
                timeout=5,
            )
        except Exception:
            pass  # never crash retry on callback failure

        raise self.retry(exc=exc, countdown=10)
