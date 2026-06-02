import os

from celery import Celery

# =========================================
# 🔥 REDIS CONFIG (ACL FIX)
# =========================================

REDIS_URL = os.getenv(
    "REDIS_URL", "redis://default:StrongRedisPassword2026!@127.0.0.1:6379/0"
)

# =========================================
# 🔥 CELERY INIT
# =========================================

celery_app = Celery("nlp_service", broker=REDIS_URL, backend=REDIS_URL)

# =========================================
# 🔥 SETTINGS
# =========================================

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    worker_prefetch_multiplier=1,
)

# =========================================
# 🔥 TASK DISCOVERY
# =========================================

celery_app.autodiscover_tasks(["app.tasks"])

try:
    import app.tasks.judgment_task

    print("✅ judgment_task loaded successfully")
except Exception as e:
    print("❌ ERROR loading judgment_task:", e)

# =========================================
# 🔥 ROUTING
# =========================================

celery_app.conf.task_routes = {
    "app.tasks.judgment_task.process_judgment": {"queue": "celery"}
}
