import re

# =========================================================
# 🔥 COURT PATTERNS
# =========================================================

SUPREME_PATTERNS = [r"IN THE SUPREME COURT OF INDIA", r"SUPREME COURT OF INDIA"]

HIGH_COURT_PATTERNS = [r"HIGH COURT OF ([A-Z ]+)", r"HIGH COURT AT ([A-Z ]+)"]

TRIBUNAL_PATTERNS = [
    (r"CENTRAL ADMINISTRATIVE TRIBUNAL", "CENTRAL ADMINISTRATIVE TRIBUNAL", "CAT"),
    (
        r"NATIONAL COMPANY LAW APPELLATE TRIBUNAL",
        "NATIONAL COMPANY LAW APPELLATE TRIBUNAL",
        "NCLAT",
    ),
    (r"NATIONAL COMPANY LAW TRIBUNAL", "NATIONAL COMPANY LAW TRIBUNAL", "NCLT"),
    (r"INCOME TAX APPELLATE TRIBUNAL", "INCOME TAX APPELLATE TRIBUNAL", "ITAT"),
    (r"SECURITIES APPELLATE TRIBUNAL", "SECURITIES APPELLATE TRIBUNAL", "SAT"),
]

# =========================================================
# 🔥 OCR NORMALIZATION
# =========================================================


def normalize_ocr(text):

    text = text.replace("—", "-")

    text = text.replace("–", "-")

    text = text.replace("|", "I")

    return text


# =========================================================
# 🔥 NORMALIZE SPACES
# =========================================================


def normalize_spaces(text):

    text = re.sub(r"\r", "\n", text)

    text = re.sub(r"\t", " ", text)

    text = re.sub(r"[ ]+", " ", text)

    text = re.sub(r"\n+", "\n", text)

    return text.strip()


# =========================================================
# 🔥 CLEAN COURT NAME
# =========================================================


def clean_court_name(name):

    if not name:

        return None

    name = re.sub(r"\s+", " ", name)

    name = name.strip(" .,-:")

    return name.title()


# =========================================================
# 🔥 EXTRACT SUPREME COURT
# =========================================================


def extract_supreme_court(header):

    for pattern in SUPREME_PATTERNS:

        if re.search(pattern, header, flags=re.I):

            return {
                "court_type": "SUPREME",
                "court_name": "Supreme Court Of India",
                "court_code": "SC",
                "confidence": 100,
            }

    return None


# =========================================================
# 🔥 EXTRACT HIGH COURT
# =========================================================


def extract_high_court(header):

    for pattern in HIGH_COURT_PATTERNS:

        match = re.search(pattern, header, flags=re.I)

        if match:

            hc_name = clean_court_name(match.group(1))

            return {
                "court_type": "HIGH_COURT",
                "court_name": f"High Court Of {hc_name}",
                "court_code": hc_name.upper().replace(" ", "_"),
                "confidence": 95,
            }

    return None


# =========================================================
# 🔥 EXTRACT TRIBUNAL
# =========================================================


def extract_tribunal(header):

    for pattern, tribunal_name, code in TRIBUNAL_PATTERNS:

        if re.search(pattern, header, flags=re.I):

            return {
                "court_type": "TRIBUNAL",
                "court_name": tribunal_name.title(),
                "court_code": code,
                "confidence": 90,
            }

    return None


# =========================================================
# 🔥 MAIN EXTRACTION
# =========================================================


def extract_court(text):

    try:

        if not text:

            return {
                "court_type": "UNKNOWN",
                "court_name": "Unknown Court",
                "court_code": "UNKNOWN",
                "confidence": 0,
            }

        # =====================================================
        # 🔥 HEADER ONLY
        # =====================================================

        header = text[:12000]

        header = normalize_ocr(header)

        header = normalize_spaces(header)

        header_upper = header.upper()

        # =====================================================
        # 🔥 SUPREME COURT
        # =====================================================

        supreme = extract_supreme_court(header_upper)

        if supreme:

            print("✅ Court Extracted:", supreme)

            return supreme

        # =====================================================
        # 🔥 HIGH COURT
        # =====================================================

        high_court = extract_high_court(header_upper)

        if high_court:

            print("✅ Court Extracted:", high_court)

            return high_court

        # =====================================================
        # 🔥 TRIBUNAL
        # =====================================================

        tribunal = extract_tribunal(header_upper)

        if tribunal:

            print("✅ Court Extracted:", tribunal)

            return tribunal

        # =====================================================
        # 🔥 FALLBACK
        # =====================================================

        return {
            "court_type": "UNKNOWN",
            "court_name": "Unknown Court",
            "court_code": "UNKNOWN",
            "confidence": 0,
        }

    except Exception as e:

        print("❌ COURT EXTRACTION ERROR:", e)

        return {
            "court_type": "UNKNOWN",
            "court_name": "Unknown Court",
            "court_code": "UNKNOWN",
            "confidence": 0,
        }
