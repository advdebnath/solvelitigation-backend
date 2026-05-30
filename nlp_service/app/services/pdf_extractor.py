import fitz

fitz.TOOLS.mupdf_display_errors(False)  # PyMuPDF
import os
from typing import Tuple


def extract_pdf_text(pdf_path: str) -> Tuple[str, str]:
    """
    Extract cleaned full text and basic HTML content from PDF.
    Returns: (full_text, html_content)
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)

    full_text_parts = []
    html_parts = []

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text")

        # Basic cleaning
        cleaned = _clean_text(text)

        full_text_parts.append(cleaned)

        # Basic HTML structure
        html_parts.append(f"<h4>Page {page_number}</h4>")
        for paragraph in cleaned.split("\n\n"):
            if paragraph.strip():
                html_parts.append(f"<p>{paragraph.strip()}</p>")

    doc.close()

    full_text = "\n\n".join(full_text_parts)
    html_content = "\n".join(html_parts)

    return full_text, html_content


def _clean_text(text: str) -> str:
    """
    Basic legal cleaning logic.
    You can enhance later.
    """

    lines = text.split("\n")

    cleaned_lines = []
    for line in lines:
        stripped = line.strip()

        # Remove empty lines
        if not stripped:
            continue

        # Remove common page number patterns
        if stripped.isdigit():
            continue

        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)
