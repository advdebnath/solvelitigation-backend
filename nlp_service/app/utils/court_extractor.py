import re


def extract_court(text: str) -> str:
    text = (text or "").upper()

    # =========================================
    # 🔥 SUPREME COURT (HIGH PRIORITY)
    # =========================================
    if "SUPREME COURT OF INDIA" in text:
        return "SUPREME COURT OF INDIA"

    # =========================================
    # 🔥 HIGH COURT (DYNAMIC DETECTION)
    # =========================================
    match = re.search(r"HIGH COURT OF [A-Z ]+", text)
    if match:
        return match.group(0).strip()

    # =========================================
    # 🔥 TRIBUNAL
    # =========================================
    if "TRIBUNAL" in text:
        return "TRIBUNAL"

    # =========================================
    # 🔥 FALLBACK (SMART GUESS)
    # =========================================
    if "APPELLATE JURISDICTION" in text:
        return "SUPREME COURT OF INDIA"

    return "UNKNOWN COURT"
