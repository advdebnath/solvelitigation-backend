print("### JUDGMENT WORKER FILE LOADED ###")
from datetime import datetime
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
    print("### ANALYZE_JUDGMENT CALLED ###", job_data)
    """
    job_data example:
    {
        "jobId": "abc123",
        "pdfPath": "/path/to/file.pdf",
        "options": {}
    }
    """

    job_id = job_data.get("jobId")
    gridfs_id = job_data.get("gridfsFileId")
    options = job_data.get("options", {})

    if not job_id:
        raise ValueError("jobId and pdfPath are required")

    print(f"[NLP] Starting job: {job_id}")
    print(f"[NLP] PDF Path: {pdf_path}")
    if not gridfs_id:\n        raise ValueError("gridfsFileId required")\n\n    from gridfs import GridFS\n    fs = GridFS(db)\n    file = fs.get(ObjectId(gridfs_id))\n    pdf_bytes = file.read()\n    print(f"[NLP] Loaded PDF from GridFS: {file.filename}")\n

    # Convert jobId to ObjectId if possible
    try:
        mongo_job_id = ObjectId(job_id)
    except Exception:
        mongo_job_id = job_id

    # -----------------------------
    # Mark job as PROCESSING
    # -----------------------------
    db.judgments.update_one(
        {"_id": mongo_job_id},
        {"$set": {"nlpStatus": "PROCESSING", "nlpStartedAt": datetime.utcnow()}},
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
        db.judgments.update_one(
            {"_id": mongo_job_id},
            {
                "$set": {
                    "nlpStatus": "COMPLETED", "nlpCompletedAt": datetime.utcnow(),
                    "result": result
                }
            }
        )

        print(f"[NLP] Job completed: {job_id}")
        return result

    except Exception as e:
        print(f"[NLP] Job failed: {job_id}")

        db.judgments.update_one(
            {"_id": mongo_job_id},
            {
                "$set": {
                    "nlpStatus": "FAILED",
                    "error": str(e),
                    "trace": traceback.format_exc()
                }
            }
        )
        raise

