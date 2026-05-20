import re

def extract_point_of_law(text, acts, sections):
    text_lower = text.lower()

    # ============================================
    # 🔥 HELPER (CONTROLLED MATCH)
    # ============================================
    def has_keywords(keywords, threshold=0.6):
        count = sum(1 for k in keywords if k in text_lower)
        return count >= max(1, int(len(keywords) * threshold))

    # ============================================
    # 🔥 STEP 1 — ACT PRIORITY (VERY IMPORTANT)
    # ============================================
    if acts:
        act = acts[0].lower()

        if "university" in act:
            return "Administrative Law – powers under University Act"

        if "delhi act" in act:
            return "Administrative Law – interpretation of Delhi Act"

        if "contract act" in act:
            # section refinement below
            pass

        if "penal code" in act:
            return "Criminal Law – offence under IPC"

    # ============================================
    # 🔥 STEP 2 — SECTION PRIORITY
    # ============================================
    if sections:
        for sec in sections:

            if "73" in sec:
                return "Contract Law – breach – damages"

            if "74" in sec:
                return "Contract Law – penalty clause"

            if "302" in sec:
                return "Criminal Law – murder"

            if "420" in sec:
                return "Criminal Law – cheating"

    # ============================================
    # 🔥 STEP 3 — CONTRACT LAW
    # ============================================
    if has_keywords(["contract", "breach", "damage"]):
        return "Contract Law – breach – damages"

    if has_keywords(["contract", "agreement", "valid"]):
        return "Contract Law – validity of agreement"

    if has_keywords(["contract", "consideration"]):
        return "Contract Law – consideration"

    # ============================================
    # 🔥 CRIMINAL LAW
    # ============================================
    if has_keywords(["murder", "homicide"]):
        return "Criminal Law – murder"

    if has_keywords(["conviction", "sentence"]):
        return "Criminal Law – conviction"

    if has_keywords(["evidence", "proof"]):
        return "Criminal Law – appreciation of evidence"

    # ============================================
    # 🔥 SERVICE LAW
    # ============================================
    if has_keywords(["termination", "service"]):
        return "Service Law – termination"

    if has_keywords(["appointment", "service"]):
        return "Service Law – appointment"

    if has_keywords(["promotion", "service"]):
        return "Service Law – promotion"

    # ============================================
    # 🔥 TAXATION
    # ============================================
    if has_keywords(["tax", "assessment"]):
        return "Taxation Law – assessment"

    if has_keywords(["gst", "tax"]):
        return "Taxation Law – GST issue"

    # ============================================
    # 🔥 ADMIN / STATUTORY FALLBACK
    # ============================================
    if acts:
        return f"{acts[0]} – interpretation of statutory provision"

    # ============================================
    # 🔥 FINAL FALLBACK
    # ============================================
    return "General Law – legal issue"
