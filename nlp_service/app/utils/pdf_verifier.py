import fitz
import difflib
from gridfs import GridFS
from bson import ObjectId
from app.db.mongo import get_db


def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def extract_text_from_gridfs(file_id: ObjectId) -> str:
    db = get_db()
    fs = GridFS(db, collection="uploads")

    grid_out = fs.get(file_id)
    pdf_bytes = grid_out.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def compare_texts(original_text: str, cleaned_text: str):
    similarity = difflib.SequenceMatcher(
        None, original_text, cleaned_text
    ).ratio()

    original_len = len(original_text)
    cleaned_len = len(cleaned_text)

    length_diff_percent = (
        abs(original_len - cleaned_len) / original_len * 100
        if original_len > 0 else 0
    )

    if similarity >= 0.99:
        status = "PASS"
    elif similarity >= 0.97:
        status = "WARNING"
    else:
        status = "FAIL"

    return {
        "verificationStatus": status,
        "similarityPercent": round(similarity * 100, 4),
        "lengthDifferencePercent": round(length_diff_percent, 4),
        "originalLength": original_len,
        "cleanedLength": cleaned_len,
    }
