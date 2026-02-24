import re

def detect_court(text: str):
    text_upper = text.upper()

    if "IN THE SUPREME COURT OF INDIA" in text_upper:
        return "Supreme Court"

    high_court_match = re.search(r"HIGH COURT OF ([A-Z\s]+)", text_upper)
    if high_court_match:
        state = high_court_match.group(1).strip()
        return f"High Court of {state.title()}"

    if "TRIBUNAL" in text_upper:
        return "Tribunal"

    return "Unknown"


def detect_category(text: str):
    text_upper = text.upper()

    if "CRIMINAL" in text_upper:
        return "Criminal"

    if "CIVIL" in text_upper:
        return "Civil"

    if "SERVICE" in text_upper:
        return "Service Law"

    if "INCOME TAX" in text_upper or "GST" in text_upper:
        return "Taxation & Corporate"

    return "General"


def extract_acts(text: str):
    acts = []

    act_patterns = [
        "INDIAN PENAL CODE",
        "CODE OF CRIMINAL PROCEDURE",
        "HINDU MARRIAGE ACT",
        "INCOME TAX ACT",
        "GST ACT",
    ]

    text_upper = text.upper()

    for act in act_patterns:
        if act in text_upper:
            acts.append(act.title())

    return acts


def compute_confidence(metadata: dict):
    confidence = 0.5

    if metadata.get("court") and metadata["court"] != "Unknown":
        confidence += 0.2

    if metadata.get("category") and metadata["category"] != "General":
        confidence += 0.2

    if metadata.get("actReferences"):
        confidence += 0.1

    return round(min(confidence, 1.0), 2)
