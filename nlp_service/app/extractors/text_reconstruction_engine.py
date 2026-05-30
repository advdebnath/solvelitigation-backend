import re

# =========================================================
# 🔥 HYPHEN REPAIR
# =========================================================


def repair_hyphenation(text):

    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    text = re.sub(r"(\w+)-\s+(\w+)", r"\1\2", text)

    return text


# =========================================================
# 🔥 MULTI-LINE JOIN
# =========================================================


def repair_line_breaks(text):

    lines = text.splitlines()

    repaired = []

    buffer = ""

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # ---------------------------------------------
        # CONTINUATION LINE
        # ---------------------------------------------

        if buffer and not re.match(r"^[A-Z0-9\(\[]", line):

            buffer += " " + line

        else:

            if buffer:
                repaired.append(buffer)

            buffer = line

    if buffer:
        repaired.append(buffer)

    return "\n".join(repaired)


# =========================================================
# 🔥 OCR NOISE CLEANER
# =========================================================


def clean_ocr_noise(text):

    replacements = {"|": "I", "§": "S", "ﬁ": "fi", "ﬂ": "fl"}

    for old, new in replacements.items():

        text = text.replace(old, new)

    # repeated dots

    text = re.sub(r"\.{2,}", ".", text)

    # repeated spaces

    text = re.sub(r"\s+", " ", text)

    return text


# =========================================================
# 🔥 CITATION WINDOW REPAIR
# =========================================================


def reconstruct_citation_windows(text):

    # SCC OnLine split repair

    text = re.sub(r"SCC\s+On\s+Line", "SCC OnLine", text, flags=re.IGNORECASE)

    # AIR split repair

    text = re.sub(r"A\s*I\s*R", "AIR", text, flags=re.IGNORECASE)

    # INSC split repair

    text = re.sub(r"I\s*N\s*S\s*C", "INSC", text, flags=re.IGNORECASE)

    return text


# =========================================================
# 🔥 MASTER ENGINE
# =========================================================


def reconstruct_legal_text(full_text="", pages=None, semantic_paragraphs=None):

    try:

        if not isinstance(full_text, str):

            full_text = str(full_text)

        original_length = len(full_text)

        # ---------------------------------------------
        # PAGE NORMALIZATION
        # ---------------------------------------------

        if pages is None:
            pages = []

        if semantic_paragraphs is None:
            semantic_paragraphs = []

        # ---------------------------------------------
        # PAGE-BASED TEXT RECONSTRUCTION
        # ---------------------------------------------

        if not full_text and pages:

            reconstructed_pages = []

            for page in pages:

                if isinstance(page, dict):

                    page_text = str(page.get("text", "")).strip()

                else:

                    page_text = str(page).strip()

                if page_text:
                    reconstructed_pages.append(page_text)

            full_text = "\n\n".join(reconstructed_pages)

        # ---------------------------------------------
        # SEMANTIC PARAGRAPH FALLBACK
        # ---------------------------------------------

        if not full_text and semantic_paragraphs:

            semantic_chunks = []

            for para in semantic_paragraphs:

                if isinstance(para, dict):

                    para_text = str(para.get("text", "")).strip()

                else:

                    para_text = str(para).strip()

                if para_text:
                    semantic_chunks.append(para_text)

            full_text = "\n\n".join(semantic_chunks)

        # ---------------------------------------------
        # PIPELINE
        # ---------------------------------------------

        full_text = repair_hyphenation(full_text)

        full_text = repair_line_breaks(full_text)

        full_text = clean_ocr_noise(full_text)

        full_text = reconstruct_citation_windows(full_text)

        print("✅ Reconstruction Complete")

        print({"original_length": original_length, "final_length": len(full_text)})

        return {"text": full_text, "confidence": 95}

    except Exception as e:

        print("❌ Reconstruction Error:")
        print(str(e))

        return {"text": full_text, "confidence": 0}
