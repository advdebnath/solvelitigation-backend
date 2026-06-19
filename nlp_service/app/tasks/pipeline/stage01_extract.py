"""
Stage 01 Extraction Layer

Owns:

- convert_pdf_to_html()
- extract_pages()

Responsibilities:

- PDF reading
- HTML extraction
- OCR fallback
- Raw caption extraction
- Page text extraction

Does NOT own:

- normalize_text()
- reconstruct_legal_text()
- semantic_segment()
- case extraction
- party extraction
- judge extraction
- date extraction
"""


import subprocess


def convert_pdf_to_html(pdf_path):

    try:

        subprocess.run(
            ["pdftohtml", "-noframes", "-stdout", pdf_path],
            capture_output=True,
            text=True,
            check=True,
        )

        result = subprocess.check_output(
            ["pdftohtml", "-noframes", "-stdout", pdf_path],
            text=True
        )

        return result

    except Exception as e:

        print("❌ HTML CONVERSION ERROR:", e)

        return ""


def extract_pages(pdf_path):
    """
    Future home of judgment_task.extract_pages()
    """
    pass


def run_stage01_extract(
    *,
    file_path,
    ingestion_id,
):
    context = {
        "ingestion_id": ingestion_id,
        "file_path": file_path,
    }

    return context
