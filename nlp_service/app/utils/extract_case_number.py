import re

def extract_case_number(text):
    patterns = [
        r"CIVIL\s+APPEAL\s+NO\.?\s*\d+\s*(OF|/)\s*\d{4}",
        r"CRIMINAL\s+APPEAL\s+NO\.?\s*\d+\s*(OF|/)\s*\d{4}",
        r"WRIT\s+PETITION.*?NO\.?\s*\d+\s*(OF|/)\s*\d{4}",
    ]

    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(0).strip()

    return "UNKNOWN"
