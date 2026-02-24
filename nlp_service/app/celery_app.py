from celery import Celery

celery_app = Celery(
    "nlp_service",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
)

# 🔥 EXPLICIT IMPORT (no autodiscover magic)
import app.tasks.judgment_task  # <-- THIS forces task registration

celery_app.conf.task_routes = {
    "app.tasks.judgment_task.process_judgment": {"queue": "nlp"}
}




