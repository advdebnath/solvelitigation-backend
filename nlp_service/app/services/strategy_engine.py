# =========================================
# ⚖️ STRATEGY ADVISOR ENGINE (UPGRADED)
# =========================================

def clean(t):
    return str(t).replace("\xa0", " ").strip()


# =========================================
# 🔥 DETERMINE CASE STRENGTH (IMPROVED)
# =========================================
def determine_strength(score):
    if score >= 70:
        return "Strong"
    elif score >= 50:
        return "Moderate"
    return "Weak"


# =========================================
# 🔥 DETECT RISKS (UPGRADED)
# =========================================
def detect_risks(cases):
    risks = []
    ratios = []

    for c in cases:
        if c.get("ratio"):
            ratios.extend(c.get("ratio"))

        if c.get("reasoning"):
            r = clean(c.get("reasoning")[0])
            if len(r) > 50:
                risks.append(r)

    # conflict detection
    if len(set(ratios)) > 1:
        risks.append("Conflicting precedents may weaken the case")

    return list(set(risks))[:3]


# =========================================
# 🔥 BUILD STRATEGY (UPGRADED)
# =========================================
def build_strategy(cases, query, outcome_score):
    if not cases:
        return "No strategy available"

    strength = determine_strength(outcome_score)

    key_points = []
    steps = []

    # =========================================
    # 🔥 EXTRACT STRONG ARGUMENTS
    # =========================================
    for c in cases:
        if c.get("ratio"):
            key_points.append(clean(c.get("ratio")[0]))

    # =========================================
    # 🔥 DETECT RISKS
    # =========================================
    risks = detect_risks(cases)

    # =========================================
    # 🔥 STRATEGY LOGIC (ADVANCED)
    # =========================================
    if strength == "Strong":
        strategy = "Proceed aggressively relying on binding precedents."

        steps = [
            "Highlight Supreme Court judgments prominently",
            "Press for final disposal or summary judgment",
            "Limit respondent arguments through precedent dominance",
            "Seek interim relief if applicable"
        ]

    elif strength == "Moderate":
        strategy = "Strengthen the case before final arguments."

        steps = [
            "Add stronger precedents (preferably Supreme Court)",
            "File additional affidavit or documents",
            "Distinguish adverse precedents",
            "Prepare strong rebuttal strategy"
        ]

    else:
        strategy = "Adopt defensive and corrective legal strategy."

        steps = [
            "Challenge applicability of adverse precedents",
            "Focus on factual distinctions",
            "Introduce new legal grounds if possible",
            "Explore settlement or alternative remedies"
        ]

    # =========================================
    # 🔥 ADD CASE-SPECIFIC STRATEGY
    # =========================================
    case_refs = []
    for c in cases[:3]:
        if c.get("ratio"):
            case_refs.append(
                f"Use {c.get('caseNumber')} to support argument: {clean(c.get('ratio')[0])}"
            )

    # =========================================
    # 🔥 FINAL OUTPUT (STRUCTURED + TEXT)
    # =========================================
    result_text = "\n🧭 STRATEGY ADVISOR\n\n"
    result_text += f"📌 Issue: {query}\n\n"
    result_text += f"📊 Case Strength: {strength}\n\n"
    result_text += f"🎯 Strategy:\n{strategy}\n\n"

    result_text += "🟢 Key Arguments:\n"
    for k in key_points[:3]:
        result_text += f"- {k}\n"

    result_text += "\n⚠️ Risks:\n"
    for r in risks:
        result_text += f"- {r}\n"

    result_text += "\n📚 Case Strategy:\n"
    for c in case_refs:
        result_text += f"- {c}\n"

    result_text += "\n📌 Next Legal Steps:\n"
    for s in steps:
        result_text += f"- {s}\n"

    # =========================================
    # 🔥 RETURN JSON + TEXT
    # =========================================
    return {
        "strength": strength,
        "strategy": strategy,
        "key_arguments": key_points[:3],
        "risks": risks,
        "case_strategy": case_refs,
        "steps": steps,
        "text": result_text
    }
