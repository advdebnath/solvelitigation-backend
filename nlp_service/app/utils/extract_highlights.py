import re


def extract_highlights(text, sections):
    paragraphs = re.split(r"\n{2,}", text)

    highlights = []

    for para in paragraphs:
        para_lower = para.lower()

        for sec in sections:
            sec_num = sec.replace("Section ", "").strip()

            patterns = [
                f"section {sec_num}",
                f"sec. {sec_num}",
                f"u/s {sec_num}",
            ]

            if any(p in para_lower for p in patterns):
                highlights.append({"section": sec, "text": para.strip()})
                break

    return highlights[:20]  # limit
