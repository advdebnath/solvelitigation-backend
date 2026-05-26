# =========================================================
# 🔥 ENTERPRISE LAYOUT-PRESERVING LEGAL EXTRACTOR
# =========================================================

import fitz
import re


# =========================================================
# 🔥 SPAN NORMALIZER
# =========================================================

def normalize_span_text(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace("\r", " ")

    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


# =========================================================
# 🔥 STRUCTURED PAGE EXTRACTION
# =========================================================

def extract_layout_preserved_text(pdf_path):

    doc = fitz.open(pdf_path)

    reconstructed_pages = []

    for page_index in range(len(doc)):

        page = doc[page_index]

        page_dict = page.get_text("dict")

        page_lines = []

        blocks = page_dict.get("blocks", [])

        for block in blocks:

            if "lines" not in block:
                continue

            for line in block["lines"]:

                spans = line.get("spans", [])

                line_parts = []

                for span in spans:

                    span_text = normalize_span_text(
                        span.get("text", "")
                    )

                    if not span_text:
                        continue

                    line_parts.append(span_text)

                if line_parts:

                    reconstructed_line = " ".join(
                        line_parts
                    )

                    reconstructed_line = re.sub(
                        r"\s+([,.;:])",
                        r"\1",
                        reconstructed_line
                    )

                    page_lines.append(
                        reconstructed_line
                    )

        page_text = "\n".join(page_lines)

        reconstructed_pages.append(page_text)

    final_text = "\n\n".join(
        reconstructed_pages
    )

    final_text = re.sub(
        r'\n{3,}',
        '\n\n',
        final_text
    )

    print("✅ ENTERPRISE LAYOUT EXTRACTION COMPLETE")

    return final_text.strip()


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:

        print("Usage:")
        print("python layout_preserving_extractor.py file.pdf")

        sys.exit(1)

    result = extract_layout_preserved_text(
        sys.argv[1]
    )

    print(result[:12000])

