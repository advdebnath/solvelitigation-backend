import os
import re
from datetime import datetime

import fitz
from app.celery_app import celery_app
from bson import ObjectId
from pymongo import MongoClient

BASE_PATH = "/var/www/solvelitigation/backend"
MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"


def get_db():
    return MongoClient(MONGO_URI)["solvelitigation"]


# =========================================
# TEXT EXTRACTION
# =========================================
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        print("❌ TEXT ERROR:", e)
        return ""


# =========================================
# PARAGRAPH ENGINE
# =========================================
def extract_paragraphs(text):
    paras = []
    raw_paras = re.split(r"\n\s*\n", text)
    for i, p in enumerate(raw_paras):
        clean = p.strip()
        if len(clean) > 100:
            paras.append({"para": i + 1, "text": clean})
    return paras


def extract_key_paragraphs(paragraphs):
    keywords = [
        "held that",
        "therefore",
        "in our opinion",
        "we find that",
        "thus",
        "it is clear",
    ]
    important = []
    for p in paragraphs:
        t = p["text"].lower()
        if any(k in t for k in keywords):
            important.append(p)
    return important[:5]


# =========================================
# CASE NUMBER
# =========================================
def extract_case_number(text):
    patterns = [
        r"CIVIL\s+APPEAL\s+NO\.?\s*\d+\s+OF\s+\d+",
        r"CRIMINAL\s+APPEAL\s+NO\.?\s*\d+\s+OF\s+\d+",
        r"SLP\s*\(.*?\).*?\d+\s+OF\s+\d+",
        r"WRIT\s+PETITION.*?\d+\s+OF\s+\d+",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group().strip()
    return None


# =========================================
# CLASSIFICATION
# =========================================
def classify_category(text):
    t = text.lower()
    if "criminal" in t or "ipc" in t:
        return "Criminal"
    if "service" in t:
        return "Service"
    if "tax" in t:
        return "Taxation & Corporate"
    return "Civil"


def detect_court(text):
    t = text.upper()
    if "SUPREME COURT" in t:
        return "SUPREME COURT OF INDIA"
    if "HIGH COURT" in t:
        return "HIGH COURT"
    return "UNKNOWN COURT"


# =========================================
# ACTS + POINTS
# =========================================
def detect_acts(text):
    t = text.lower()
    acts = set()
    if "ipc" in t or "302" in t:
        acts.add("Indian Penal Code")
    if "contract" in t:
        acts.add("Contract Act")
    if "138" in t:
        acts.add("Negotiable Instruments Act")
    return list(acts)


def extract_points(text):
    t = text.lower()
    points = []
    if "murder" in t:
        points.append("Criminal Law – Murder")
    if "contract" in t:
        points.append("Contract – Breach")
    if "cheque" in t:
        points.append("Cheque Bounce")
    if not points:
        points.append("General Issue")
    return list(set(points))


# =========================================
# HEADNOTE (UPGRADED)
# =========================================
def generate_headnote(text, category, key_paras):
    t = text.lower()
    topics = []

    if "murder" in t:
        topics.append("Murder")
    if "contract" in t:
        topics.append("Contract")
    if "cheque" in t:
        topics.append("Cheque Bounce")

    if not topics:
        topics.append("General Issue")

    topic_str = " – ".join(topics[:3])

    para_ref = ""
    if key_paras:
        para_ref = f"(para-{key_paras[0]['para']})"

    return f"{category} – {topic_str} – decision rendered {para_ref}"


# =========================================
# MAIN TASK
# =========================================
@celery_app.task(name="app.tasks.judgment_task.process_judgment")
def process_judgment(ingestion_id: str):
    db = get_db()

    try:
        print("🔥 NLP TASK STARTED:", ingestion_id)

        ingestion = db.judgmentingestions.find_one({"_id": ObjectId(ingestion_id)})
        if not ingestion:
            raise Exception("❌ Ingestion not found")

        pdf_path = os.path.join(BASE_PATH, ingestion["file"]["relativePath"])

        text = extract_text_from_pdf(pdf_path)

        if not text or len(text) < 500:
            raise Exception("❌ TEXT EXTRACTION FAILED")

        print("📄 TEXT LENGTH:", len(text))

        paragraphs = extract_paragraphs(text)
        key_paras = extract_key_paragraphs(paragraphs)

        case_number = extract_case_number(text)
        if not case_number:
            case_number = (
                f"UNRESOLVED_{ingestion_id}_{int(datetime.utcnow().timestamp())}"
            )

        category = classify_category(text)
        court = detect_court(text)

        acts = detect_acts(text)
        points = extract_points(text)
        headnote = generate_headnote(text, category, key_paras)

        existing = db.judgments.find_one({"caseNumber": case_number})
        if existing:
            case_number = f"{case_number}_{ingestion_id}"

        db.judgments.insert_one(
            {
                "caseNumber": case_number,
                "category": category,
                "court": court,
                "acts": acts,
                "headnote": headnote,
                "pointsOfLaw": points,
                "paragraphs": paragraphs,
                "keyParagraphs": key_paras,
                "fullText": text,
                "createdAt": datetime.utcnow(),
            }
        )

        print("✅ INSERTED:", case_number)

        db.judgmentingestions.update_one(
            {"_id": ObjectId(ingestion_id)},
            {
                "$set": {
                    "status": "COMPLETED",
                    "stage": "COMPLETED",
                    "progress": 100,
                    "completedAt": datetime.utcnow(),
                    "nlpProcessed": True,
                    "isCompleted": True,
                }
            },
        )

    except Exception as e:
        print("❌ ERROR:", str(e))
