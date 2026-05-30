import re

# =====================================================
# 🔥 DETECT OUTCOME
# =====================================================


def detect_outcome(text: str) -> str:

    lower = text.lower()

    outcome_patterns = [
        ("appeal dismissed", "Appeal Dismissed"),
        ("appeal allowed", "Appeal Allowed"),
        ("petition dismissed", "Petition Dismissed"),
        ("petition allowed", "Petition Allowed"),
        ("set aside", "Order Set Aside"),
        ("conviction upheld", "Conviction Upheld"),
        ("acquitted", "Accused Acquitted"),
        ("bail granted", "Bail Granted"),
        ("bail rejected", "Bail Rejected"),
        ("matter remanded", "Matter Remanded"),
        ("disposed of", "Matter Disposed"),
        ("writ petition allowed", "Writ Petition Allowed"),
        ("writ petition dismissed", "Writ Petition Dismissed"),
    ]

    for phrase, result in outcome_patterns:

        if phrase in lower:

            return result

    return "Order Passed"


# =====================================================
# 🔥 SELECT IMPORTANT POINTS
# =====================================================


def select_key_points(points_of_law):

    if not points_of_law:

        return []

    priority_keywords = [
        "IPC",
        "NDPS",
        "CrPC",
        "Negotiable Instruments",
        "Bail",
        "Murder",
        "Cheque Dishonour",
        "Specific Performance",
        "Arbitration",
        "Tax",
        "Constitution",
        "Service",
        "Termination",
        "Reinstatement",
        "Dowry",
        "Corruption",
    ]

    selected = []

    # =============================================
    # 🔥 PRIORITY MATCHES
    # =============================================

    for keyword in priority_keywords:

        for point in points_of_law:

            if keyword.lower() in point.lower():

                if point not in selected:

                    selected.append(point)

    # =============================================
    # 🔥 FALLBACK
    # =============================================

    if not selected:

        selected = points_of_law[:3]

    return selected[:5]


# =====================================================
# 🔥 GENERATE HEADNOTE
# =====================================================


def generate_headnote(category: str, acts: list, points_of_law: list, text: str):

    try:

        parts = []

        # =============================================
        # 🔥 CATEGORY
        # =============================================

        if category:

            parts.append(category)

        # =============================================
        # 🔥 ACTS
        # =============================================

        important_acts = acts[:2]

        for act in important_acts:

            if act not in parts:

                parts.append(act)

        # =============================================
        # 🔥 POINTS OF LAW
        # =============================================

        selected_points = select_key_points(points_of_law)

        for point in selected_points:

            if point not in parts:

                parts.append(point)

        # =============================================
        # 🔥 OUTCOME
        # =============================================

        outcome = detect_outcome(text)

        if outcome not in parts:

            parts.append(outcome)

        # =============================================
        # 🔥 FINAL HEADNOTE
        # =============================================

        headnote = " – ".join(parts)

        # CLEAN SPACES

        headnote = re.sub(r"\s+", " ", headnote)

        return headnote.strip()

    except Exception as e:

        print("❌ HEADNOTE GENERATION ERROR:", e)

        return "Legal Issue Involved"
