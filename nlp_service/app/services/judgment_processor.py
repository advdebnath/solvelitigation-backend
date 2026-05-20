from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os, re, subprocess, shutil
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"
BASE_PATH = "/var/www/solvelitigation/backend"

def get_db():
    return MongoClient(MONGO_URI)["solvelitigation"]

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model

def generate_embedding(text):
    try:
        model = get_embedding_model()
        emb = model.encode(text[:2000])
        return emb.tolist() if emb is not None else []
    except:
        return []

def extract_number(f):
    match = re.search(r"-(\d+)\.html$", f)
    return int(match.group(1)) if match else 0

def find_all_html_files(base):
    files = []
    directory = os.path.dirname(base)
    prefix = os.path.basename(base).replace(".pdf", "")

    if not os.path.exists(directory):
        return []

    for f in os.listdir(directory):
        if f.startswith(prefix) and f.endswith(".html"):
            files.append(os.path.join(directory, f))

    return sorted(files, key=extract_number)

def extract_from_html(base):
    html_files = find_all_html_files(base)
    if not html_files:
        return ""

    full_text = []

    for html_path in html_files:
        try:
            with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f, "html.parser")

            for tag in soup.find_all(["div", "span", "p"]):
                t = tag.get_text(" ", strip=True)
                if t and len(t) > 5:
                    full_text.append(t)

        except:
            pass

    text = " ".join(full_text)
    return re.sub(r"\s+", " ", text).strip()

def extract_with_ocr(pdf_path):
    try:
        tmp_dir = pdf_path + "_ocr_tmp"
        os.makedirs(tmp_dir, exist_ok=True)

        result = subprocess.run(
            ["pdftoppm", "-png", pdf_path, os.path.join(tmp_dir, "page")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return ""

        import pytesseract
        from PIL import Image

        text_parts = []

        for img in os.listdir(tmp_dir):
            if img.endswith(".png"):
                txt = pytesseract.image_to_string(Image.open(os.path.join(tmp_dir, img)))
                if txt:
                    text_parts.append(txt)

        shutil.rmtree(tmp_dir, ignore_errors=True)

        return re.sub(r"\s+", " ", " ".join(text_parts)).strip()

    except:
        return ""

def extract_text(pdf_path):
    base = pdf_path.replace(".pdf", "")

    html_text = extract_from_html(base)
    ocr_text = ""

    if len(html_text) < 200:
        ocr_text = extract_with_ocr(pdf_path)

    if html_text and ocr_text:
        text = html_text + " " + ocr_text
    elif ocr_text:
        text = ocr_text
    else:
        text = html_text

    return re.sub(r"\s+", " ", text).strip()

def process_judgment_core(ingestion_id):
    db = get_db()

    try:
        oid = ObjectId(ingestion_id)

        ingestion = db.judgmentingestions.find_one({"_id": oid})
        if not ingestion:
            raise Exception("Ingestion not found")

        file_path = os.path.join(BASE_PATH, ingestion["file"]["relativePath"])

        text = extract_text(file_path)

        if len(text) < 200:
            raise Exception("Extraction too weak")

        embedding = generate_embedding(text)

        db.judgments.update_one(
            {"ingestionId": oid},
            {
                "$set": {
                    "fullText": text[:100000],
                    "embedding": embedding,
                    "createdAt": datetime.utcnow()
                }
            },
            upsert=True
        )

        return True

    except Exception as e:
        db.judgmentingestions.update_one(
            {"_id": ObjectId(ingestion_id)},
            {"$set": {"status": "FAILED", "error": str(e)}}
        )
        return False
