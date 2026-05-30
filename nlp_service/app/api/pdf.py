import os
import tempfile
import traceback

# 🔥 EXISTING IMPORT
from app.pdf.generate_pdf import generate_judgment_pdf
# 🔥 NEW IMPORT
from app.services.fact_extractor import extract_all
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()

# ============================================
# 🔥 MODELS
# ============================================


class PDFRequest(BaseModel):
    judgment: dict
    user: dict


class TextRequest(BaseModel):
    text: str


# ============================================
# 🔥 SAFE FILE STREAM
# ============================================


def stream_file(path: str):
    try:
        with open(path, "rb") as f:
            yield from f
    finally:
        if os.path.exists(path):
            os.remove(path)


# ============================================
# 🔥 PDF GENERATION (EXISTING - IMPROVED)
# ============================================


@router.post("/generate-pdf")
def generate_pdf_endpoint(payload: PDFRequest):
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_path = temp_file.name
        temp_file.close()

        generate_judgment_pdf(
            judgment=payload.judgment,
            user=payload.user,
            output_path=temp_path,
        )

        return StreamingResponse(
            stream_file(temp_path),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=judgment.pdf"},
        )

    except Exception as e:
        print("❌ PDF ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="PDF generation failed")


# ============================================
# 🔥 FACT EXTRACTION API (NEW - CRITICAL)
# ============================================


@router.post("/extract-facts")
def extract_facts_api(payload: TextRequest):
    try:
        text = payload.text

        if not text or len(text.strip()) < 10:
            return {"success": False, "message": "Text too short"}

        result = extract_all(text)

        return {"success": True, "data": result}

    except Exception as e:
        print("❌ FACT EXTRACTION ERROR:", traceback.format_exc())
        return {"success": False, "message": "Extraction failed"}


# ============================================
# 🔥 HEALTH CHECK (OPTIONAL BUT USEFUL)
# ============================================


@router.get("/pdf-health")
def pdf_health():
    return {"status": "ok", "service": "pdf_and_fact_service"}
