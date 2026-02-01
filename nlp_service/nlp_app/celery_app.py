import os
from celery import Celery

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", BROKER_URL)

celery_app = Celery(
    "nlp_app",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["nlp_app.tasks"],
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_default_queue="nlp",
    task_routes={
        "nlp_app.tasks.*": {"queue": "nlp"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_prefetch_multiplier=1,
    task_ignore_result=False,
    timezone="UTC",
    enable_utc=True,
)
