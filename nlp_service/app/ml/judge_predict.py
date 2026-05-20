from pymongo import MongoClient
from typing import List, Dict, Optional

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"

client = MongoClient(MONGO_URI)
db = client["solvelitigation"]


# ============================================
# 🔥 NORMALIZE JUDGE NAME
# ============================================

def normalize_judge_name(name: str) -> str:
    return name.strip().upper()


# ============================================
# 🔥 CORE JUDGE PREDICTION (SINGLE JUDGE)
# ============================================

def _single_judge_prediction(judge_name: str) -> Optional[Dict]:
    judge_name = normalize_judge_name(judge_name)

    cases = list(db.judgments.find({
        "judgeList": judge_name,
        "outcome": {"$ne": None}
    }))

    if len(cases) == 0:
        return None

    wins = sum(1 for c in cases if c.get("outcome") == 1)
    total = len(cases)

    probability = int((wins / total) * 100)

    return {
        "judge": judge_name,
        "cases": total,
        "wins": wins,
        "probability": probability
    }


# ============================================
# 🔥 MAIN FUNCTION (SINGLE OR MULTI-JUDGE)
# ============================================

def predict_with_judge(judge_input: Optional[str]):
    if not judge_input:
        return None

    # 🔥 Split multiple judges if provided
    judges = [j.strip() for j in judge_input.split(",") if j.strip()]

    results = []

    for j in judges:
        res = _single_judge_prediction(j)
        if res:
            results.append(res)

    if not results:
        return None

    # ============================================
    # 🔥 COMBINE MULTIPLE JUDGES (AVERAGE)
    # ============================================

    avg_probability = int(sum(r["probability"] for r in results) / len(results))

    total_cases = sum(r["cases"] for r in results)

    # ============================================
    # 🔥 CONFIDENCE LEVEL
    # ============================================

    if total_cases > 20:
        confidence = "High"
    elif total_cases > 10:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "finalProbability": avg_probability,
        "confidence": confidence,
        "judgeBreakdown": results,
        "totalCases": total_cases
    }
