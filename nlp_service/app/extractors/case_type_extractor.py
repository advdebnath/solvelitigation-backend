from app.legal_ontology.supreme_court_case_types import \
    detect_supreme_court_case_type

# =========================================================
# 🔥 GENERIC CASE TYPE EXTRACTOR
# =========================================================


def extract_case_type(text, court=None, jurisdiction=None):

    try:

        if not text:
            return {}

        text = str(text)

        if court and "SUPREME COURT" in court.upper():

            result = detect_supreme_court_case_type(text)

            return result or {}

        return {}

    except Exception as e:

        print("❌ CASE TYPE EXTRACTION ERROR:", e)

        return {}
