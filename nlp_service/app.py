# ================================
#   SOLVELITIGATION NLP SERVICE
# ================================

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from rq import Queue
import redis

# -----------------------
# Initialize Flask app
# -----------------------
app = Flask(__name__)
CORS(app)

# -----------------------
# MongoDB Connection
# -----------------------
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://127.0.0.1:27017/solvelitigation"
)

db = None
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.get_database()
    print("INFO: Connected to MongoDB")
except Exception as e:
    print(f"ERROR: MongoDB connection failed: {e}")

# -----------------------
# Redis + RQ
# -----------------------
redis_conn = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True
)

nlp_queue = Queue("nlp-jobs", connection=redis_conn)

# -----------------------
# Enqueue NLP Job
# -----------------------
@app.route("/enqueue", methods=["POST"])
def enqueue_job():
    data = request.get_json(silent=True)

    if not data or "jobId" not in data or "pdfPath" not in data:
        return jsonify({
            "success": False,
            "message": "jobId and pdfPath required"
        }), 400

    nlp_queue.enqueue(
        "workers.judgment_worker.analyze_judgment",
        data
    )

    return jsonify({
        "success": True,
        "queued": True,
        "jobId": data.get("jobId")
    })

# -----------------------
# Health Check
# -----------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "ok": True,
        "service": "nlp",
        "mongo": db is not None,
        "redis": redis_conn.ping()
    })

# -----------------------
# Root
# -----------------------
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "SolveLitigation NLP API",
        "status": "running"
    })

# -----------------------
# Main (IMPORTANT)
# -----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
