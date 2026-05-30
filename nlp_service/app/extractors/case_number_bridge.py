# =========================================================
# 🔥 CASE NUMBER BRIDGE ENGINE
# =========================================================

from app.extractors.case_number_extractor import \
    extract_case_number as legacy_extract_case_number
from app.extractors.judicial.judicial_router import extract_case_number_v2


def extract_case_number_bridge(text):

    # =====================================================
    # 🔥 TRY V2 FIRST
    # =====================================================

    try:

        result = extract_case_number_v2(text)

        if result and result.get("validation_passed"):

            print("🔥 V2 EXTRACTION SUCCESS 🔥")

            return result

    except Exception as e:

        print("❌ V2 EXTRACTION FAILED:")
        print(str(e))

    # =====================================================
    # 🔥 FALLBACK TO LEGACY ENGINE
    # =====================================================

    print("⚠️ FALLING BACK TO LEGACY ENGINE ⚠️")

    return legacy_extract_case_number(text)
