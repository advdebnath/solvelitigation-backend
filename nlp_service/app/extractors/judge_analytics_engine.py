# =========================================================
# 🔥 JUDGE ANALYTICS ENGINE
# =========================================================

import re
from collections import Counter


def extract_judge_analytics(
    full_text,
    judges=None,
    operative_order_data=None,
    headnote_data=None,
    semantic_issues=None,
):

    try:

        if judges is None:
            judges = []

        if not isinstance(judges, list):
            judges = []

        lower_text = re.sub(r"\\s+", " ", full_text.lower())

        print("✅ Judge Analytics Normalized Text Sample:")
        print(lower_text[:1000])

        # =====================================================

        traits = []

        # =====================================================
        # 🔥 STRUCTURED OPERATIVE ORDER ANALYSIS
        # =====================================================

        operative_text = ""

        if isinstance(operative_order_data, dict):

            operative_text = str(operative_order_data.get("final_holding", "")).lower()

        print("✅ OPERATIVE TEXT:")
        print(operative_text)

        if any(x in operative_text for x in ["high court set aside", "set aside"]):

            traits.append("Appellate Interventionist")

        if any(x in operative_text for x in ["appeal allowed", "allowed"]):

            traits.append("Rights-Oriented")

        if any(x in operative_text for x in ["dismissed"]):

            traits.append("Restrictive")

        # 🔥 TRAIT DETECTION
        # =====================================================

        if any(
            x in lower_text
            for x in [
                "allowed",
                "appeal allowed",
                "petition allowed",
                "set aside",
                "quashed",
                "relief granted",
                "writ petition allowed" "relief granted",
            ]
        ):

            traits.append("Liberal Relief Approach")

        if any(
            x in lower_text
            for x in [
                "dismissed",
                "appeal dismissed",
                "petition dismissed",
                "no merit",
                "liable to be dismissed",
                "cannot be accepted",
                "interference not warranted" "rejected",
            ]
        ):

            traits.append("Strict Interpretation")

        if any(
            x in lower_text
            for x in [
                "article 226",
                "writ petition",
                "constitutional remedy",
                "fundamental rights",
                "maintainability of writ petition",
                "high court",
                "article 227",
                "judicial review",
                "constitutional jurisdiction",
            ]
        ):

            traits.append("Constitutional Activism")

        if any(
            x in lower_text
            for x in [
                "natural justice",
                "fair hearing",
                "procedural fairness",
                "audi alteram partem",
            ]
        ):

            traits.append("Procedural Fairness Focus")

        if any(
            x in lower_text
            for x in [
                "tribunal",
                "special tribunal",
                "jurisdiction of tribunal",
                "wakf tribunal",
                "tribunal adjudication",
                "special forum",
                "alternative remedy",
            ]
        ):

            traits.append("Tribunal Deference")

        if any(
            x in lower_text
            for x in ["liberty", "personal liberty", "human rights", "civil rights"]
        ):

            traits.append("Civil Liberties Expansion")

        # =====================================================
        # 🔥 TRAIT COUNTS
        # =====================================================

        trait_scores = dict(Counter(traits))

        primary_tendency = None

        if trait_scores:

            primary_tendency = max(trait_scores, key=trait_scores.get)

        # =====================================================
        # 🔥 APPEAL RATE
        # =====================================================

        appeal_allowance_rate = 50

        if "allowed" in lower_text:

            appeal_allowance_rate = 100

        elif "dismissed" in lower_text:

            appeal_allowance_rate = 0

        # =====================================================
        # 🔥 RESPONSE
        # =====================================================

        return {
            "judges": judges,
            "primary_tendency": primary_tendency,
            "judicial_traits": list(trait_scores.keys()),
            "trait_scores": trait_scores,
            "appeal_allowance_rate": appeal_allowance_rate,
        }

    except Exception as e:

        print("❌ Judge Analytics Error:")

        print(e)

        return {
            "judges": [],
            "primary_tendency": None,
            "judicial_traits": [],
            "trait_scores": {},
            "appeal_allowance_rate": 50,
        }
