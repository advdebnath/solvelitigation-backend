from app.celery_app import celery_app
from app.services.judgment_processor import process_judgment_core
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId  # ✅ FIX

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"

def get_db():
    return MongoClient(MONGO_URI)["solvelitigation"]

@celery_app.task(
    name="app.tasks.judgment_task.process_judgment",
    bind=True,
    max_retries=3
)
def process_judgment(self, ingestion_id: str):
    db = get_db()

    try:
        print("🚀 TASK START:", ingestion_id)

        # ============================================
        # 🔥 MARK PROCESSING
        # ============================================
        db.judgmentingestions.update_one(
            {"_id": ObjectId(ingestion_id)},   # ✅ FIXED
            {
                "$set": {
                    "status": "PROCESSING",
                    "stage": "EXTRACTION",
                    "processingAt": datetime.utcnow(),
                    "progress": 10
                }
            }
        )

        # ============================================
        # 🔥 CORE PROCESSING
        # ============================================
        result = process_judgment_core(ingestion_id)

        if not result:
            raise Exception("Processing returned False")

        # ============================================
        # 🔥 SUCCESS UPDATE
        # ============================================
        db.judgmentingestions.update_one(
            {"_id": ObjectId(ingestion_id)},   # ✅ FIXED
            {
                "$set": {
                    "status": "COMPLETED",
                    "stage": "DONE",
                    "progress": 100,
                    "completedAt": datetime.utcnow(),
                    "error": None
                }
            }
        )

        print("✅ TASK COMPLETED:", ingestion_id)

    except Exception as e:
        print("❌ TASK ERROR:", ingestion_id, e)

        # ============================================
        # 🔥 FAILURE UPDATE
        # ============================================
        db.judgmentingestions.update_one(
            {"_id": ObjectId(ingestion_id)},   # ✅ FIXED
            {
                "$set": {
                    "status": "FAILED",
                    "stage": "ERROR",
                    "error": str(e),
                    "failedAt": datetime.utcnow()
                }
            }
        )

        # ============================================
        # 🔥 RETRY LOGIC
        # ============================================
        try:
            print("🔁 Retrying...")
            self.retry(exc=e, countdown=5)
        except Exception as retry_error:
            print("❌ Retry failed:", retry_error)
