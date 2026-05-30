import re
from typing import Dict, List


def extract_legal_metadata(text: str) -> Dict:

    metadata = {
        "category": None,
        "acts": [],
        "sections": [],
        "pointsOfLaw": [],
        "caseRelations": {
            "overruled": [],
            "reliedOn": [],
            "referred": [],
            "distinguished": [],
            "followed": [],
            "affirmed": [],
            "reversed": [],
        },
        "summary": None,
        "confidence": 0.6,
    }

    text_lower = text.lower()

    # ---------------------------
    # Category Detection
    # ---------------------------
    if "ipc" in text_lower or "criminal appeal" in text_lower:
        metadata["category"] = "Criminal"
    elif "writ petition" in text_lower or "civil appeal" in text_lower:
        metadata["category"] = "Civil"
    elif "service matter" in text_lower:
        metadata["category"] = "Service"
    elif "income tax" in text_lower or "gst" in text_lower:
        metadata["category"] = "Taxation & Corporate"
    else:
        metadata["category"] = "General"

    # ---------------------------
    # Acts Extraction
    # ---------------------------
    act_patterns = [
        r"Indian Penal Code",
        r"Code of Criminal Procedure",
        r"Code of Civil Procedure",
        r"Income Tax Act",
        r"GST Act",
        r"Companies Act",
        r"Transfer of Property Act",
        r"Constitution of India",
    ]

    for pattern in act_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            if m not in metadata["acts"]:
                metadata["acts"].append(m)

    # ---------------------------
    # Section Extraction
    # ---------------------------
    section_matches = re.findall(r"Section\s+\d+[A-Za-z\-]*", text)
    metadata["sections"] = list(set(section_matches))

    # ---------------------------
    # Points of Law (Basic Heuristic)
    # ---------------------------
    if "conviction" in text_lower:
        metadata["pointsOfLaw"].append("Conviction validity")
    if "bail" in text_lower:
        metadata["pointsOfLaw"].append("Grant of bail")
    if "reinstatement" in text_lower:
        metadata["pointsOfLaw"].append("Reinstatement in service")
    if "assessment" in text_lower:
        metadata["pointsOfLaw"].append("Tax assessment validity")

    # ---------------------------
    # Case Relationship Detection
    # ---------------------------
    relation_patterns = {
        "overruled": r"overruled",
        "reliedOn": r"relied on",
        "referred": r"referred to",
        "distinguished": r"distinguished",
        "followed": r"followed",
        "affirmed": r"affirmed",
        "reversed": r"reversed",
    }

    for relation, pattern in relation_patterns.items():
        matches = re.findall(pattern, text_lower)
        if matches:
            metadata["caseRelations"][relation].append("Detected")

    # ---------------------------
    # Simple Summary (First 5 lines)
    # ---------------------------
    lines = text.strip().split("\n")
    metadata["summary"] = " ".join(lines[:5])[:1000]

    return metadata
