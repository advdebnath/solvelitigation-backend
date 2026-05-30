# =========================================
# 🔥 IMPORTS
# =========================================
import os

from app.db.mongo import get_db
from app.services.advocate_engine import build_arguments
from app.services.judge_engine import generate_judgment
from app.services.multi_case_reasoning import multi_case_analysis
from app.services.outcome_engine import predict_outcome
from app.services.strategy_engine import build_strategy


# =========================================
# 🔥 SAFE STRING HANDLER
# =========================================
def safe_str(val):
    if isinstance(val, dict):
        return val.get("reason", str(val))
    if isinstance(val, list):
        return " ".join([str(v) for v in val])
    return str(val)


# =========================================
# 🔥 FALLBACK LEGAL KNOWLEDGE
# =========================================
def basic_legal_explanation(query: str) -> str:
    q = query.lower()

    if "interpretation of statute" in q:
        return (
            "Interpretation of statute refers to how courts understand "
            "legislative intent. The primary rules are:\n"
            "1. Literal Rule\n"
            "2. Golden Rule\n"
            "3. Mischief Rule\n"
            "Courts also consider purposive interpretation."
        )

    if "contract" in q:
        return "A contract is an agreement enforceable by law under the Indian Contract Act."

    if "murder" in q:
        return "Murder is punishable under Section 302 IPC."

    return "Legal interpretation depends on statutory language, facts, and judicial precedents."


# =========================================
# 🔥 REAL SEARCH FUNCTION (MONGODB)
# =========================================
def search_similar_cases(query: str, limit: int = 5):
    try:
        db = get_db()
        judgments_collection = db["judgments"]

        # 🔥 TEXT SEARCH
        results = list(
            judgments_collection.find(
                {"$text": {"$search": query}},
                {"caseNumber": 1, "headnote": 1, "pointsOfLaw": 1, "category": 1},
            ).limit(limit)
        )

        # 🔥 FALLBACK (regex)
        if not results:
            results = list(
                judgments_collection.find(
                    {"headnote": {"$regex": query, "$options": "i"}},
                    {"caseNumber": 1, "headnote": 1, "pointsOfLaw": 1, "category": 1},
                ).limit(limit)
            )

        return results

    except Exception as e:
        print("❌ search_similar_cases error:", e)
        return []


# =========================================
# 🔥 MAIN LEGAL GPT ENGINE
# =========================================
def generate_legal_answer(query: str):
    try:
        cases = search_similar_cases(query)

        if not cases:
            fallback = basic_legal_explanation(query)

            return (
                "\n📊 LEGAL ANALYSIS (FALLBACK)\n\n"
                "No direct case found.\n\n"
                "================ BASIC LAW =================\n" + fallback
            )

        multi = multi_case_analysis(cases)
        advocate = build_arguments(cases, query)
        judgment = generate_judgment(cases, query)
        outcome = predict_outcome(cases, query)
        strategy = build_strategy(cases, query, 50)

        result = "\n📊 LEGAL ANALYSIS\n\n"

        result += "================ MULTI CASE =================\n"
        result += safe_str(multi) + "\n\n"

        result += "================ ADVOCATE =================\n"
        result += safe_str(advocate) + "\n\n"

        result += "================ JUDGMENT =================\n"
        result += safe_str(judgment) + "\n\n"

        result += "================ OUTCOME =================\n"
        result += safe_str(outcome) + "\n\n"

        result += "================ STRATEGY =================\n"
        result += safe_str(strategy) + "\n\n"

        return result

    except Exception as e:
        return f"❌ Error in Legal GPT Engine: {str(e)}"
