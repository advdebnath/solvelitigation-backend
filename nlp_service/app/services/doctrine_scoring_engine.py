# =========================================================
# 🔥 DOCTRINAL SCORING ENGINE
# =========================================================

import re

from app.legal_ontology.doctrinal_ontology import DOCTRINAL_ONTOLOGY

# =========================================================
# 🔥 MAIN ENGINE
# =========================================================


def detect_doctrines(full_text, acts=None, sections=None):

    if not isinstance(full_text, str):
        full_text = str(full_text)

    lower_text = full_text.lower()

    acts = acts or []
    sections = sections or []

    doctrine_scores = {}

    # =====================================================
    # 🔥 SCORING
    # =====================================================

    for doctrine, config in DOCTRINAL_ONTOLOGY.items():

        score = 0

        # -------------------------------------------------
        # KEYWORDS
        # -------------------------------------------------

        for keyword in config.get("keywords", []):

            if keyword.lower() in lower_text:
                score += 10

        # -------------------------------------------------
        # ACTS
        # -------------------------------------------------

        for act in config.get("acts", []):

            for extracted_act in acts:

                if act.lower() in str(extracted_act).lower():
                    score += 20

        # -------------------------------------------------
        # SECTIONS
        # -------------------------------------------------

        for sec in config.get("sections", []):

            for extracted_sec in sections:

                if sec.lower() in str(extracted_sec).lower():
                    score += 15

        # -------------------------------------------------
        # FINALIZE
        # -------------------------------------------------

        if score > 0:

            doctrine_scores[doctrine] = {
                "score": score,
                "category": config.get("category"),
            }

    # =====================================================
    # 🔥 SORT
    # =====================================================

    sorted_doctrines = sorted(
        doctrine_scores.items(), key=lambda x: x[1]["score"], reverse=True
    )

    dominant_doctrine = sorted_doctrines[0][0] if sorted_doctrines else "UNDETERMINED"

    return {"dominant_doctrine": dominant_doctrine, "all_doctrines": sorted_doctrines}
