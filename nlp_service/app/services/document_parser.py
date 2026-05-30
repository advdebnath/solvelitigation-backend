import re


def extract_paragraphs(text):
    paragraphs = re.split(r"\n\s*\n", text)

    structured = []

    for i, p in enumerate(paragraphs):
        if len(p.strip()) > 20:
            structured.append({"para_no": i + 1, "text": p.strip()})

    return structured


def extract_annexures(text):
    pattern = r"Annexure[-\s]*([A-Z0-9]+)"
    matches = re.findall(pattern, text, re.IGNORECASE)

    return list(set(matches))


def parse_document(text):
    return {
        "paragraphs": extract_paragraphs(text),
        "annexures": extract_annexures(text),
    }
