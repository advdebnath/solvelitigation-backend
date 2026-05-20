# =========================================================
# 🔥 CONFIDENCE + CONTRADICTION ENGINE
# =========================================================

def build_confidence_object(
    value=None,
    confidence=0,
    contradictions=None,
    evidence=None
):

    if contradictions is None:
        contradictions = []

    if evidence is None:
        evidence = []

    return {
        "value": value,
        "confidence": confidence,
        "contradictions": contradictions,
        "evidence": evidence,
        "review_recommended": confidence < 60
    }

