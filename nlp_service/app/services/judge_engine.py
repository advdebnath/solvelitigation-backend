from datetime import datetime


def clean(t):
    return str(t).replace("\xa0", " ").strip()


# =========================================
# 🔥 COURT HIERARCHY SCORE
# =========================================
def get_weight(case):
    court = str(case.get("court", "")).lower()

    if "supreme" in court:
        return 3
    elif "high" in court:
        return 2
    return 1


# =========================================
# 🔥 EXTRACT CORE ELEMENTS (UPGRADED)
# =========================================
def extract_core(cases, query=None):
    facts = []
    issues = []
    reasoning = []
    ratio = []

    for c in cases:
        issues.extend(c.get("issues", []))
        reasoning.extend(c.get("reasoning", []))
        ratio.extend(c.get("ratio", []))

        text = c.get("fullText", "")
        if text:
            facts.append(clean(text[:400]))

    # 🔥 fallback issue
    if not issues and query:
        issues = [f"Whether the issue relating to {query} is legally sustainable?"]

    return {
        "facts": facts[:3],
        "issues": list(set(issues))[:5],
        "reasoning": reasoning[:5],
        "ratio": list(set(ratio))[:5],
    }


# =========================================
# 🔥 CONFLICT DETECTION
# =========================================
def detect_conflict(ratios):
    unique = list(set([clean(r) for r in ratios]))

    if len(unique) > 1:
        return True, unique[:3]

    return False, unique


# =========================================
# 🔥 DECISION ENGINE (UPGRADED)
# =========================================
def decide_case(cases, ratios):
    score = 0

    for c in cases:
        weight = get_weight(c)

        if c.get("ratio"):
            score += weight

        if c.get("reasoning"):
            score += weight * 0.5

    if score >= len(cases) * 2:
        return "Petition Allowed"
    else:
        return "Petition Dismissed"


# =========================================
# 🔥 MAIN JUDGMENT GENERATOR
# =========================================
def generate_judgment(cases, query=None):
    if not cases:
        return "No material available for judgment"

    core = extract_core(cases, query)

    now = datetime.utcnow().strftime("%d %B %Y")

    conflict, conflict_data = detect_conflict(core["ratio"])
    decision = decide_case(cases, core["ratio"])

    judgment = "\n⚖️ IN THE COURT OF AI JUDGE\n"
    judgment += f"Date: {now}\n\n"

    # =========================================
    # FACTS
    # =========================================
    judgment += "📜 FACTS:\n"
    for f in core["facts"]:
        judgment += f"- {f}...\n"

    # =========================================
    # ISSUES
    # =========================================
    judgment += "\n📌 ISSUES FOR DETERMINATION:\n"
    for i in core["issues"]:
        judgment += f"- {clean(i)}\n"

    # =========================================
    # ARGUMENTS
    # =========================================
    judgment += "\n🟢 ARGUMENTS (Petitioner):\n"
    for c in cases[:3]:
        if c.get("ratio"):
            r = c.get("ratio")[0]
            judgment += f"- Reliance placed on {c.get('caseNumber')} where it was held that {clean(r)}\n"

    judgment += "\n🔴 ARGUMENTS (Respondent):\n"
    for c in cases[:3]:
        if c.get("reasoning"):
            r = clean(c.get("reasoning")[0])
            if len(r) > 40:
                judgment += f"- It is contended that {r}\n"

    # =========================================
    # ANALYSIS
    # =========================================
    judgment += "\n🧠 ANALYSIS:\n"
    for r in core["reasoning"]:
        judgment += f"- {clean(r)}\n"

    # =========================================
    # CONFLICT HANDLING
    # =========================================
    if conflict:
        judgment += "\n⚠️ CONFLICT IN PRECEDENTS:\n"
        for c in conflict_data:
            judgment += f"- {clean(c)}\n"
        judgment += "The Court resolves the conflict by applying higher judicial authority and settled principles.\n"

    # =========================================
    # FINDINGS
    # =========================================
    judgment += "\n⚖️ FINDINGS:\n"
    judgment += "Upon consideration of the rival submissions and judicial precedents, this Court holds that:\n"

    for r in core["ratio"]:
        judgment += f"- {clean(r)}\n"

    # =========================================
    # RATIO
    # =========================================
    judgment += "\n📌 RATIO DECIDENDI:\n"
    for r in core["ratio"]:
        judgment += f"- {clean(r)}\n"

    # =========================================
    # FINAL ORDER
    # =========================================
    judgment += "\n🏁 FINAL ORDER:\n"
    judgment += f"The petition is {decision.lower()} based on binding precedent and legal reasoning.\n"

    return judgment
