from celery import shared_task
from app.config import settings


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
    retry_backoff=True,
    retry_jitter=True,
    name="app.tasks.judgment_task.process_judgment",
)
def process_judgment(self, ingestion_id: str):

    from app.db.repositories import update_ingestion_status
    from app.services.backend_client import BackendClient

    backend = BackendClient(settings.BACKEND_CALLBACK_URL)

    # Mark processing started
    update_ingestion_status(ingestion_id, status="PROCESSING")

    # --- Simulated NLP work ---
    # (replace with real logic later)

    # Mark completed
    update_ingestion_status(ingestion_id, status="COMPLETED")

    backend.send_status({
        "ingestionId": ingestion_id,
        "status": "COMPLETED"
    })

    return {
        "ingestionId": ingestion_id,
        "status": "COMPLETED",
    }
