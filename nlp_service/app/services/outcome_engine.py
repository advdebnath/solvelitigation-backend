from app.services.precedent_engine import assign_weight


def clean(t):
    return str(t).replace("\xa0", " ").strip()


# =========================================
# 🔥 SCORE CALCULATION (UPGRADED)
# =========================================
def calculate_strength(cases):
    if not cases:
        return 50

    total_score = 0
    max_possible = len(cases) * 30  # dynamic scaling

    ratios = []

    for c in cases:
        weight = assign_weight(c)

        ratio = c.get("ratio") or []
        reasoning = c.get("reasoning") or []

        if ratio:
            total_score += weight * 10
            ratios.extend([clean(r) for r in ratio])

        if reasoning:
            total_score += weight * 5

    # 🔥 CONFLICT PENALTY
    if len(set(ratios)) > 1:
        total_score -= 10

    # normalize safely
    score = (total_score / max_possible) * 100 if max_possible else 50

    return round(max(0, min(100, score)), 2)


# =========================================
# 🔥 DETERMINE SIDE (IMPROVED)
# =========================================
def decide_side(cases):
    petitioner_score = 0
    respondent_score = 0

    for c in cases:
        weight = assign_weight(c)

        if c.get("ratio"):
            petitioner_score += weight * 2

        if c.get("reasoning"):
            respondent_score += weight

    if petitioner_score > respondent_score:
        return "Petitioner"
    elif respondent_score > petitioner_score:
        return "Respondent"
    return "Balanced"


# =========================================
# 🔥 CONFIDENCE LEVEL (UPGRADED)
# =========================================
def confidence_level(score):
    if score >= 70:
        return "High"
    elif score >= 50:
        return "Moderate"
    return "Low"


# =========================================
# 🔥 EXPLANATION ENGINE
# =========================================
def build_reasons(cases):
    reasons = []
    ratios = []

    for c in cases:
        if c.get("ratio"):
            ratios.extend(c.get("ratio"))

    if ratios:
        reasons.append("Strong binding precedents identified")

    if len(set(ratios)) > 1:
        reasons.append("Conflicting judicial interpretations exist")

    if not reasons:
        reasons.append("Balanced legal position")

    return reasons[:3]


# =========================================
# 🔥 FINAL OUTCOME ENGINE (UPGRADED)
# =========================================
def predict_outcome(cases, query):
    if not cases:
        return {
            "probability": 50,
            "decision": "Uncertain",
            "confidence": "Low",
            "analysis": "No data available"
        }

    score = calculate_strength(cases)
    side = decide_side(cases)
    confidence = confidence_level(score)
    reasons = build_reasons(cases)

    # =========================================
    # 🔥 DECISION LABEL
    # =========================================
    if score >= 65:
        decision = f"Likely in favour of {side}"
    elif score >= 50:
        decision = "Leaning but uncertain"
    elif score >= 40:
        decision = "Risky case"
    else:
        decision = f"Likely against {side}"

    # =========================================
    # 🔥 TEXT OUTPUT (FOR UI)
    # =========================================
    text = "\n📊 OUTCOME ANALYSIS\n\n"
    text += f"📌 Issue: {query}\n\n"
    text += f"🏆 Likely Outcome: {decision}\n"
    text += f"📈 Strength Score: {score}/100\n"
    text += f"🔍 Confidence Level: {confidence}\n\n"

    text += "⚖️ KEY REASONS:\n"
    for r in reasons:
        text += f"- {r}\n"

    # =========================================
    # 🔥 RETURN BOTH JSON + TEXT
    # =========================================
    return {
        "probability": score,
        "decision": decision,
        "confidence": confidence,
        "reasons": reasons,
        "text": text
    }
