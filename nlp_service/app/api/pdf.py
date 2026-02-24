from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.pdf.generate_pdf import generate_judgment_pdf
import tempfile
import os

router = APIRouter()


class PDFRequest(BaseModel):
    judgment: dict
    user: dict


@router.post("/generate-pdf")
def generate_pdf_endpoint(payload: PDFRequest):
    try:
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_path = temp_file.name
        temp_file.close()

        # Generate PDF
        generate_judgment_pdf(
            judgment=payload.judgment,
            user=payload.user,
            output_path=temp_path,
        )

        # Stream PDF safely
        def file_iterator():
            try:
                with open(temp_path, "rb") as f:
                    yield from f
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        return StreamingResponse(
            file_iterator(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=judgment.pdf"
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
