import fitz  # PyMuPDF
import re
import json

def remove_watermarks_and_signatures(doc):
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            page.clean_contents()
        blocks = page.get_text("blocks")
        for b in blocks:
            text = b[4].strip().lower()
            if any(keyword in text for keyword in ["signed", "barcode", "confidential", "digital", "certified", "signature"]):
                page.add_redact_annot(b[:4], fill=(255, 255, 255))
        page.apply_redactions()

def extract_toc(doc):
    toc = doc.get_toc()
    return [{"title": t[1], "page": t[2]} for t in toc] if toc else []

def extract_footnotes(text):
    footnote_pattern = r"(?:\n|\r|\s)(\d+)\s+([^.\n]+(?:\.\s+[^.\n]+)*)"
    return re.findall(footnote_pattern, text)

def process_pdf_to_json(pdf_path):
    doc = fitz.open(pdf_path)
    remove_watermarks_and_signatures(doc)

    pages_content = []
    all_text = ""

    for i, page in enumerate(doc):
        text = page.get_text()
        all_text += text + "\n"

        images = []
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            images.append({
                "image_name": f"page_{i+1}_img_{xref}.png",
                "image_bytes_base64": base_image["image"].hex(),  # Optional: convert to base64
                "width": base_image["width"],
                "height": base_image["height"]
            })

        pages_content.append({
            "page_number": i + 1,
            "text": text,
            "images": images
        })

    toc = extract_toc(doc)
    footnotes = extract_footnotes(all_text)

    return {
        "total_pages": len(doc),
        "toc": toc,
        "footnotes": [{"ref": num, "content": content} for num, content in footnotes],
        "pages": pages_content
    }
