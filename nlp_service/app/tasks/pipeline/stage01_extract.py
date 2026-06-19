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

    try:

        import fitz

        doc = fitz.open(pdf_path)

        pages = []

        raw_caption_text = ""

        max_pages = min(len(doc), 300)

        print("✅ TOTAL PDF PAGES:")
        print(len(doc))

        print("✅ EXTRACTING PAGES:")
        print(max_pages)

        for page_num in range(max_pages):

            page = doc[page_num]

            # =================================================
            # 🔒 LAYOUT-AWARE CAPTION BLOCK EXTRACTION
            # =================================================

            if page_num == 0:
                raw_caption_text = ""

            if page_num <= 1:

                try:

                    blocks = page.get_text("blocks")

                    caption_lines = []

                    for block in blocks:

                        try:

                            block_text = str(block[4]).strip()

                            if not block_text:
                                continue

                            caption_lines.append(block_text)

                        except Exception:
                            pass

                    raw_caption_text += "\n".join(caption_lines) + "\n"

                    print(f"🔥 RAW BLOCK CAPTION PAGE {page_num + 1}:\n")

                    print(raw_caption_text[:8000])

                except Exception as block_error:

                    print("❌ BLOCK CAPTION EXTRACTION ERROR:")

                    print(str(block_error))

            page_text = page.get_text("text")

            # ================================================
            # 🔒 IMMUTABLE RAW CAPTION PRESERVATION
            # ================================================

            if page_num == 0:

                raw_first_page_snapshot = str(page_text)

                print("🔥 IMMUTABLE FIRST PAGE SNAPSHOT:")
                print(raw_first_page_snapshot[:12000])

            # =================================================
            # 🔥 RAW FIRST PAGE DEBUG
            # =================================================

            if page_num == 0:

                print(f"🔥 RAW PAGE-1 TEXT FROM FITZ:\n{page_text[:8000]}")

            # -------------------------------------------------
            # 🔥 OCR FALLBACK
            # -------------------------------------------------

            if not page_text or len(page_text.strip()) < 50:

                try:

                    pix = page.get_pixmap()

                    import tempfile

                    import pytesseract
                    from PIL import Image

                    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:

                        pix.save(tmp.name)

                        image = Image.open(tmp.name)

                        ocr_text = pytesseract.image_to_string(image)

                        if ocr_text.strip():

                            page_text = ocr_text

                            print(f"✅ OCR USED PAGE {page_num + 1}")

                except Exception as ocr_error:

                    print("❌ OCR ERROR:", str(ocr_error))

            pages.append(page_text)

        doc.close()

        print("✅ TOTAL EXTRACTED PAGES:")
        print(len(pages))

        print("✅ TOTAL TEXT LENGTH:")
        print(sum(len(str(p)) for p in pages))

        return pages, raw_caption_text

    except Exception as e:

        print("❌ PAGE EXTRACTION ERROR:", e)

        return []

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
