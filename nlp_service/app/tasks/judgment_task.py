from app.utils.judge_normalizer import normalize_judges
import hashlib
import html
import fitz
import re
import logging

from gridfs import GridFS
from datetime import datetime
from bson import ObjectId

from app.celery_app import celery_app
from app.db.mongo import get_db
from app.db.repositories import (
    get_ingestion_by_id,
    update_ingestion_status,
)

logger = logging.getLogger(__name__)

# ===============================
# NLP CLEANING
# ==============================


def prepare_text_for_nlp(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"\s+", " ", text)
    cleaned = re.sub(r"Digitally signed by.*?Reason:", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


# ===============================
# METADATA DETECTION
# ===============================

def detect_court(text: str):
    text_upper = text.upper()

    if "IN THE SUPREME COURT OF INDIA" in text_upper:
        return "Supreme Court"

    high_court_match = re.search(r"HIGH COURT OF ([A-Z\s]+)", text_upper)
    if high_court_match:
        state = high_court_match.group(1).strip()
        return f"High Court of {state.title()}"

    if "NATIONAL COMPANY LAW TRIBUNAL" in text_upper:
        return "NCLT"

    if "TRIBUNAL" in text_upper:
        return "Tribunal"

    return "Unknown"


def detect_category(text: str):
    text_upper = text.upper()

    if "CRIMINAL APPEAL" in text_upper or "INDIAN PENAL CODE" in text_upper:
        return "Criminal"

    if "TRANSFER PETITION" in text_upper or "CIVIL APPEAL" in text_upper:
        return "Civil"

    if "SERVICE MATTER" in text_upper or "SERVICE LAW" in text_upper:
        return "Service Law"

    if "INCOME TAX" in text_upper or "GST" in text_upper:
        return "Taxation & Corporate"

    if "HINDU MARRIAGE ACT" in text_upper:
        return "Civil"

    return "General"


def extract_case_number(text: str):
    patterns = [
        r"CIVIL APPEAL NO\.?\s*[\w./-]+\s*of\s*\d{4}",
        r"CRIMINAL APPEAL NO\.?\s*[\w./-]+\s*of\s*\d{4}",
        r"SLP\(C\)\s*No\.?\s*[\w./-]+\s*of\s*\d{4}",
        r"TRANSFER PETITION.*?NO\.?\s*[\w./-]+\s*of\s*\d{4}",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()

    return None

import re

def extract_judges_from_text(text: str):
    judges = set()

    # 1️⃣ Extract from signature block [Name]
    signature_matches = re.findall(r"\[\s*([A-Za-z\.\s]+?)\s*\]", text)
    for match in signature_matches:
        name = match.strip()
        if is_valid_judge_name(name):
            judges.add(normalize_name(name))

    # 2️⃣ Extract from “J U D G M E N T” section
    judgment_section_match = re.search(
        r"J\s*U\s*D\s*G\s*M\s*E\s*N\s*T(.+?)(\n\d|\nLeave|\nThese|\Z)",
        text,
        re.DOTALL
    )

    if judgment_section_match:
        section_text = judgment_section_match.group(1)

        lines = section_text.split("\n")
        for line in lines:
            line = line.strip()

            if line.endswith(", J") or line.endswith(",J"):
                name = line.replace(", J", "").replace(",J", "").strip()
                if is_valid_judge_name(name):
                    judges.add(normalize_name(name))

    return list(judges)


def is_valid_judge_name(name: str) -> bool:
    if len(name) < 5:
        return False

    # Reject noise words
    noise_words = [
        "video", "signed", "reportable", "emphasis",
        "court master", "ar-cum", "ten years",
        "who has", "file", "order"
    ]

    lower = name.lower()
    for word in noise_words:
        if word in lower:
            return False

    # Must contain alphabet only (no numbers)
    if re.search(r"\d", name):
        return False

    # Must start with capital letter
    if not name[0].isupper():
        return False

    return True


def normalize_name(name: str) -> str:
    # Remove extra spaces
    name = re.sub(r"\s+", " ", name)

    # Remove honorific prefixes for clean storage
    name = name.replace("HON'BLE", "").replace("Hon'ble", "").strip()

    return name

def extract_judgment_date(text: str):
    patterns = [
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}",
        r"\b\d{2}\.\d{2}\.\d{4}\b",
        r"\b\d{1,2}\s+\w+\s+\d{4}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()

    return None


def extract_acts(text: str):
    acts = []
    act_patterns = [
        "INDIAN PENAL CODE",
        "CODE OF CRIMINAL PROCEDURE",
        "HINDU MARRIAGE ACT",
        "INCOME TAX ACT",
        "GOODS AND SERVICES TAX ACT",
        "GST ACT",
    ]

    text_upper = text.upper()

    for act in act_patterns:
        if act in text_upper:
            acts.append(act.title())

    return list(set(acts))


def compute_confidence(metadata: dict):
    score = 0.5

    if metadata.get("court") and metadata["court"] != "Unknown":
        score += 0.15

    if metadata.get("category") and metadata["category"] != "General":
        score += 0.15

    if metadata.get("actReferences"):
        score += 0.1

    if metadata.get("caseNumber"):
        score += 0.1

    return round(min(score, 0.95), 2)


# ===============================
# CELERY TASK
# ===============================

@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
    retry_backoff=True,
    retry_jitter=True,
    name="app.tasks.judgment_task.process_judgment",
)
def process_judgment(self, ingestion_id: str):

    logger.info(f"📥 Starting processing | ingestion_id={ingestion_id}")

    db = get_db()
    ingestion_obj_id = ObjectId(ingestion_id)

    update_ingestion_status(ingestion_id, status="PROCESSING")

    ingestion = get_ingestion_by_id(ingestion_id)
    if not ingestion:
        return

    gridfs_id = ingestion.get("file", {}).get("gridfsFileId")
    if not gridfs_id:
        update_ingestion_status(ingestion_id, status="FAILED", error="Missing gridfsFileId")
        return

    fs = GridFS(db, collection="judgments")
    grid_file = fs.find_one({"_id": gridfs_id})

    if not grid_file:
        update_ingestion_status(ingestion_id, status="FAILED", error="PDF not found in GridFS")
        return

    try:
        pdf_bytes = grid_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        full_text = ""
        html_pages = []

        for page in doc:
            text = page.get_text()
            full_text += text + "\n"
            escaped = html.escape(text)
            html_pages.append(f"<section class='page'><pre>{escaped}</pre></section>")

        html_content = "<html><body>" + "".join(html_pages) + "</body></html>"

        clean_text = prepare_text_for_nlp(full_text)

        metadata = {}
        metadata["court"] = detect_court(clean_text)
        metadata["category"] = detect_category(clean_text)
        metadata["caseNumber"] = extract_case_number(clean_text)
        metadata["judgmentDate"] = extract_judgment_date(clean_text)
        metadata["judges"] = extract_judges(full_text)
        metadata["judges"] = normalize_judges(metadata.get("judges", []))
        metadata["actReferences"] = extract_acts(clean_text)
        metadata["confidence"] = compute_confidence(metadata)

        page_count = len(doc)
        text_length = len(full_text)
        checksum = hashlib.sha256(pdf_bytes).hexdigest()

    except Exception as e:
        update_ingestion_status(ingestion_id, status="FAILED", error=str(e))
        raise

    existing = db["judgments"].find_one({"ingestionId": ingestion_obj_id}, {"_id": 1})

    judgment_data = {
        "ingestionId": ingestion_obj_id,
        "htmlContent": html_content,
        "pageCount": page_count,
        "textLength": text_length,
        "checksum": checksum,
        "nlpStatus": "COMPLETED",
        "category": metadata["category"],
        "court": metadata["court"],
        "caseNumber": metadata.get("caseNumber"),
        "judgmentDate": metadata.get("judgmentDate"),
        "judges": metadata.get("judges", []),
        "actReferences": metadata["actReferences"],
        "summary": full_text[:500],
        "confidence": metadata["confidence"],
        "updatedAt": datetime.utcnow(),
    }

    if existing:
        db["judgments"].update_one({"_id": existing["_id"]}, {"$set": judgment_data})
    else:
        judgment_data["createdAt"] = datetime.utcnow()
        db["judgments"].insert_one(judgment_data)

    update_ingestion_status(ingestion_id, status="COMPLETED")

    logger.info(f"✅ Completed | ingestion_id={ingestion_id}")

# ==========================
# HIGH COURT JUDGE EXTRACTION
# ==========================

import re

def extract_high_court_judges(text: str):
    judges = set()

    # Extract from CORAM block
    coram_match = re.search(
        r"CORAM\s*:?\s*(.+?)(\n\n|\nDate|\nReserved|\nPronounced|\Z)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if coram_match:
        coram_text = coram_match.group(1)
        lines = coram_text.split("\n")
        for line in lines:
            name = clean_high_court_line(line)
            if name:
                judges.add(name)

    # Extract from BEFORE block
    before_match = re.search(
        r"BEFORE\s*(.+?)(\n\n|\nDate|\nReserved|\Z)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if before_match:
        before_text = before_match.group(1)
        lines = before_text.split("\n")
        for line in lines:
            name = clean_high_court_line(line)
            if name:
                judges.add(name)

    return list(judges)


def clean_high_court_line(line: str):
    line = line.strip()

    if "JUSTICE" not in line.upper():
        return None

    line = re.sub(r"HON'?BLE", "", line, flags=re.IGNORECASE)
    line = re.sub(r"THE", "", line, flags=re.IGNORECASE)
    line = re.sub(r"MR\.?|MS\.?|MRS\.?", "", line, flags=re.IGNORECASE)
    line = re.sub(r"JUSTICE", "", line, flags=re.IGNORECASE)

    line = re.sub(r"\s+", " ", line).strip()

    if len(line) < 5:
        return None

    return line

