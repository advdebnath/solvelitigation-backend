from collections import Counter
from app.services.precedent_engine import get_strongest_case, resolve_conflict


# =========================================
# 🔥 CLEAN HELPERS
# =========================================
def clean_text(t):
    return str(t).replace("\xa0", " ").strip()


def safe_str(val):
    if isinstance(val, dict):
        return val.get("reason", str(val))
    if isinstance(val, list):
        return " ".join([str(v) for v in val])
    return str(val)


# =========================================
# 🔥 COURT PRIORITY
# =========================================
def get_weight(case):
    court = str(case.get("courtType", "")).lower()

    if "supreme" in court:
        return 3
    elif "high" in court:
        return 2
    return 1


# =========================================
# 🔥 REMOVE DUPLICATES
# =========================================
def unique_cases(cases):
    seen = {}
    for c in cases:
        key = c.get("caseNumber")
        if key and key not in seen:
            seen[key] = c
    return list(seen.values())


# =========================================
# 🔥 GROUP BY CATEGORY
# =========================================
def group_by_category(cases):
    grouped = {}

    for c in cases:
        cat = c.get("category", "Unknown")
        grouped.setdefault(cat, []).append(c)

    return grouped


# =========================================
# 🔥 DOMINANT RATIO (WEIGHTED)
# =========================================
def dominant_ratio(cases):
    weighted = []

    for c in cases:
        weight = get_weight(c)

        for r in c.get("ratio", []):
            weighted.extend([clean_text(r)] * weight)

    if not weighted:
        return ["No clear ratio found"]

    most_common = Counter(weighted).most_common(3)
    return [safe_str(r[0]) for r in most_common]


# =========================================
# 🔥 CONFLICT DETECTION
# =========================================
def detect_conflict(cases):
    ratios = []

    for c in cases:
        if c.get("ratio"):
            ratios.append(" ".join([safe_str(x) for x in c.get("ratio")]).lower())

    unique = list(set(ratios))

    if len(unique) > 1:
        return True, unique[:2]

    return False, unique


# =========================================
# 🔥 SYNTHESIS
# =========================================
def synthesize(cases):
    reasoning = []

    for c in cases:
        reasoning.extend(c.get("reasoning", []))

    clean_reasoning = []
    for r in reasoning:
        r = clean_text(r)

        if any(x in r.lower() for x in ["article", "section", "rule"]):
            continue

        clean_reasoning.append(r)

    clean_reasoning = list(dict.fromkeys(clean_reasoning))

    return clean_reasoning[:5]


# =========================================
# 🔥 MAIN ENGINE
# =========================================
def multi_case_analysis(cases):
    if not cases:
        return "No cases found"

    cases = unique_cases(cases)

    grouped = group_by_category(cases)

    result = "\n⚖️ MULTI-CASE ANALYSIS\n\n"

    for category, group in grouped.items():

        result += f"\n📂 Category: {category}\n"

        for c in group[:3]:
            court = safe_str(c.get("courtType", "UNKNOWN"))

            ratio = c.get("ratio", [])
            ratio_text = safe_str(ratio[0])[:200] if ratio else "No ratio"

            result += f"\n🔹 Case: {safe_str(c.get('caseNumber'))} ({court})\n"
            result += f"   Ratio: {ratio_text}\n"

        dom = dominant_ratio(group)
        result += f"\n📌 Dominant Principle: {', '.join([safe_str(d) for d in dom])}\n"

        conflict, _ = detect_conflict(group)

        if conflict:
            result += "\n⚠️ Conflict detected between precedents\n"
        else:
            result += "\n✔ Consistent legal position\n"

        syn = synthesize(group)

        result += "\n🧠 Synthesized Reasoning:\n"
        for r in syn:
            result += f"- {safe_str(r)}\n"

    # =========================================
    # 🔥 PRECEDENT HIERARCHY
    # =========================================
    strongest = get_strongest_case(cases)

    if strongest:
        result += "\n🏆 STRONGEST PRECEDENT:\n"
        result += f"{safe_str(strongest.get('caseNumber'))} ({safe_str(strongest.get('courtType'))})\n"

    winner, note = resolve_conflict(cases)

    result += "\n⚖️ PRECEDENCE DECISION:\n"
    result += safe_str(note) + "\n"

    # =========================================
    # 🔥 FINAL CONCLUSION
    # =========================================
    conflict, _ = detect_conflict(cases)

    if conflict:
        conclusion = "There exists judicial conflict requiring careful interpretation."
    else:
        conclusion = "The legal position is consistent and supported by binding precedents."

    result += "\n📌 FINAL CONCLUSION:\n"
    result += conclusion

    return result
