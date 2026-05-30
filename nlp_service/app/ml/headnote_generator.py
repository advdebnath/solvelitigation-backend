import re


# ============================================
# 🔥 DECISION DETECTION (STRONG)
# ============================================
def infer_decision(text: str):
    text_lower = text.lower()

    if "appeal dismissed" in text_lower:
        return "Appeal dismissed"
    if "appeal allowed" in text_lower:
        return "Appeal allowed"
    if "petition dismissed" in text_lower:
        return "Petition dismissed"
    if "petition allowed" in text_lower:
        return "Petition allowed"
    if "conviction upheld" in text_lower:
        return "Conviction upheld"
    if "acquitted" in text_lower:
        return "Accused acquitted"

    return "Decision rendered"


# ============================================
# 🔥 ISSUE DETECTION
# ============================================
def extract_issue(text: str):
    text_lower = text.lower()

    if "breach" in text_lower and "contract" in text_lower:
        return "Whether there was breach of contract"
    if "agreement" in text_lower:
        return "Whether a valid agreement exists"
    if "cheque" in text_lower:
        return "Whether cheque dishonour offence is made out"
    if "murder" in text_lower:
        return "Whether offence of murder is established"

    return "Legal issue involved"


# ============================================
# 🔥 IMPROVED HEADNOTE GENERATOR
# ============================================
def generate_headnote(category, acts, points, full_text=None):
    try:
        parts = []

        # ============================================
        # 🔹 CATEGORY
        # ============================================
        if category:
            parts.append(f"{category} Law")
        else:
            parts.append("General Law")

        # ============================================
        # 🔹 ACT
        # ============================================
        if acts:
            parts.append(acts[0])

        # ============================================
        # 🔹 POINT PRIORITIZATION (IMPROVED)
        # ============================================
        important_points = []

        for p in points:
            if any(
                k in p.lower()
                for k in ["contract", "breach", "liability", "cheque", "murder"]
            ):
                important_points.append(p)

        if not important_points:
            important_points = points

        parts.extend(important_points[:2])

        # ============================================
        # 🔹 ISSUE (NEW)
        # ============================================
        issue = extract_issue(full_text or "")
        parts.append(issue)

        # ============================================
        # 🔹 BUILD BASE
        # ============================================
        headnote = " – ".join(parts)

        # ============================================
        # 🔹 HELD (COURT STYLE)
        # ============================================
        decision = infer_decision(full_text or "")
        headnote += f" – Held: {decision}"

        return headnote

    except Exception as e:
        print("⚠️ HEADNOTE ERROR:", e)
        return ""
