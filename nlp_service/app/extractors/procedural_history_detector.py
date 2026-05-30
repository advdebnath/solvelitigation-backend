import re
from typing import Dict, List

# =========================================================
# 🔥 PROCEDURAL HISTORY DETECTOR
# =========================================================


def detect_procedural_history(text: str) -> List[Dict]:

    if not text:
        return []

    paragraphs = re.split(r"\n{2,}", text)

    results = []

    for para in paragraphs:

        clean_para = para.strip()

        if len(clean_para) < 40:
            continue

        lower_para = clean_para.lower()

        stage = None

        # =====================================================
        # 🔥 TRIAL COURT
        # =====================================================

        if any(
            x in lower_para
            for x in [
                "trial court",
                "learned trial court",
                "sessions court",
                "convicted by",
                "acquitted by",
            ]
        ):

            stage = "TRIAL_COURT"

        # =====================================================
        # 🔥 SUPREME COURT FINAL
        # =====================================================

        elif any(
            x in lower_para
            for x in [
                "we therefore allow",
                "the appeal is allowed",
                "the appeals are allowed",
                "appeal stands allowed",
                "we accordingly allow",
                "appeal deserves to be allowed",
            ]
        ):

            stage = "SUPREME_COURT_FINAL"

        # =====================================================
        # 🔥 HIGH COURT
        # =====================================================

        elif any(
            x in lower_para
            for x in [
                "high court",
                "division bench",
                "single judge",
                "dismissed by the high court",
                "allowed by the high court",
            ]
        ):

            stage = "HIGH_COURT"

        # =====================================================
        # 🔥 STORE
        # =====================================================

        if stage:

            results.append({"stage": stage, "text": clean_para[:2000]})

    return results
