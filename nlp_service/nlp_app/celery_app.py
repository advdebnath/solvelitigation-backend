# app/celery_app.py
import os
from celery import Celery

BROKER_URL = (
    os.getenv("CELERY_BROKER_URL")
    or os.getenv("REDIS_URL")
    or "redis://127.0.0.1:6379/0"
)
RESULT_URL = os.getenv("CELERY_RESULT_BACKEND", BROKER_URL)

celery_app = Celery(
    "nlp",
    broker=BROKER_URL,
    backend=RESULT_URL,
    include=["app.tasks"],          # <-- only the real module path
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_default_queue="nlp",
    task_routes={
        "tasks.*": {"queue": "nlp"},       # if you named tasks like "tasks.summarize"
        "app.tasks.*": {"queue": "nlp"},   # if you left default names ("app.tasks.summarize")
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_prefetch_multiplier=1,
    task_ignore_result=False,  # ensure .get() works
    timezone="UTC",
    enable_utc=True,
)
