import re


def clean(text: str):
    return re.sub(r"\s+", " ", text).strip()


def extract_parties(text: str):
    m = re.search(r"(.+?)\s+Versus\s+(.+?)(?:\n|$)", text, re.IGNORECASE)
    if m:
        return {"petitioner": clean(m.group(1)), "respondent": clean(m.group(2))}
    return {}


def extract_date(text: str):
    m = re.search(r"\b(\d{1,2}[/-][A-Za-z]{3}[/-]\d{2,4})\b", text)
    return m.group(1) if m else ""


def extract_section(text: str, keyword: str):
    m = re.search(rf"{keyword}[:\-]?\s*(.+?)(?:\n\n|\.\s|\n[A-Z])", text, re.IGNORECASE)
    return clean(m.group(1)) if m else ""


def extract_facts(text: str):
    facts = extract_section(text, "facts")
    if not facts:
        # fallback: first 500 chars
        facts = text[:500]
    return facts


def extract_relief(text: str):
    relief = extract_section(text, "prayer|relief")
    return relief


def extract_issues(text: str):
    issues = []
    matches = re.findall(r"(whether.+?\?)", text, re.IGNORECASE)
    for m in matches:
        issues.append(clean(m))
    return issues[:3]


def extract_all(text: str):
    parties = extract_parties(text)

    return {
        "petitioner": parties.get("petitioner", ""),
        "respondent": parties.get("respondent", ""),
        "date": extract_date(text),
        "facts": extract_facts(text),
        "issues": extract_issues(text),
        "relief": extract_relief(text),
    }
