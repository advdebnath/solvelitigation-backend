import os
from dotenv import load_dotenv

load_dotenv("/var/www/solvelitigation/nlp_service/.env")

from celery import Celery
from kombu import Queue
from app.config import settings

celery_app = Celery(
    settings.NLP_SERVICE_NAME,
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,

    # 🔥 DECLARE QUEUES EXPLICITLY
    task_default_queue="nlp",
    task_queues=[
        Queue("nlp"),
    ],

    task_routes={
        "app.tasks.judgment_task.process_judgment": {"queue": "nlp"},
    },
)

import app.tasks.judgment_task  # noqa
