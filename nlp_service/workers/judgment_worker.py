# =========================================
# SolveLitigation NLP – Judgment RQ Worker
# =========================================

import redis
from pymongo import MongoClient
from bson import ObjectId
import traceback

# -----------------------------
# Redis connection
# -----------------------------
redis_conn = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True
)

# -----------------------------
# MongoDB connection
# -----------------------------
mongo = MongoClient("mongodb://127.0.0.1:27017/solvelitigation")
db = mongo.get_database()

# =====================================================
# Core NLP job function (RQ ENTRY POINT)
# MUST MATCH enqueue string:
# "workers.judgment_worker.analyze_judgment"
# =====================================================
def analyze_judgment(job_data: dict):
    """
    job_data example:
    {
        "jobId": "abc123",
        "pdfPath": "/path/to/file.pdf",
        "options": {}
    }
    """

    job_id = job_data.get("jobId")
    pdf_path = job_data.get("pdfPath")
    options = job_data.get("options", {})

    if not job_id or not pdf_path:
        raise ValueError("jobId and pdfPath are required")

    print(f"[NLP] Starting job: {job_id}")
    print(f"[NLP] PDF Path: {pdf_path}")

    # Convert jobId to ObjectId if possible
    try:
        mongo_job_id = ObjectId(job_id)
    except Exception:
        mongo_job_id = job_id

    # -----------------------------
    # Mark job as PROCESSING
    # -----------------------------
    db.nlpjobs.update_one(
        {"_id": mongo_job_id},
        {"$set": {"status": "PROCESSING"}},
        upsert=True
    )

    try:
        # ==================================
        # PLACEHOLDER – NLP PIPELINE
        # ==================================
        # Later plug:
        # - PDF cleanup
        # - OCR
        # - Headnotes
        # - Points of Law
        # ==================================

        result = {
            "summary": "Summary placeholder – to be generated",
            "pointsOfLaw": [],
            "acts": []
        }


        # -----------------------------
        # Mark job as COMPLETED
        # -----------------------------
        db.nlpjobs.update_one(
            {"_id": mongo_job_id},
            {
                "$set": {
                    "status": "COMPLETED",
                    "result": result
                }
            }
        )

        print(f"[NLP] Job completed: {job_id}")
        return result

    except Exception as e:
        print(f"[NLP] Job failed: {job_id}")

        db.nlpjobs.update_one(
            {"_id": mongo_job_id},
            {
                "$set": {
                    "status": "FAILED",
                    "error": str(e),
                    "trace": traceback.format_exc()
                }
            }
        )
        raise

