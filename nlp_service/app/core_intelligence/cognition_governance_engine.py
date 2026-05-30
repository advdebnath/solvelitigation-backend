# =========================================================
# 🔥 LEGAL COGNITION GOVERNANCE ENGINE
# =========================================================


def evaluate_cognition_governance(
    optimization_profile, evolution_data, harmonized_output
):

    governance = {
        "system_safe": True,
        "requires_human_review": False,
        "constitutional_overreach_risk": False,
        "semantic_drift_risk": False,
        "unstable_agents": [],
        "governance_actions": [],
        "governance_score": 1.0,
    }

    try:

        # =====================================================
        # 🔥 SYSTEM STABILITY
        # =====================================================

        stability = optimization_profile.get("system_stability", 1.0)

        if stability < 0.50:

            governance["system_safe"] = False

            governance["requires_human_review"] = True

            governance["governance_actions"].append("stability_review_required")

        # =====================================================
        # 🔥 CONSTITUTIONAL OVERREACH
        # =====================================================

        constitutional_growth = evolution_data.get("constitutional_growth_index", 0.0)

        if constitutional_growth > 0.90:

            governance["constitutional_overreach_risk"] = True

            governance["governance_actions"].append("constitutional_rebalancing")

        # =====================================================
        # 🔥 SEMANTIC DRIFT
        # =====================================================

        confidence_spread = harmonized_output.get("confidence_spread", 0.0)

        if confidence_spread > 0.60:

            governance["semantic_drift_risk"] = True

            governance["requires_human_review"] = True

            governance["governance_actions"].append("semantic_arbitration_review")

        # =====================================================
        # 🔥 UNSTABLE AGENTS
        # =====================================================

        weak_agents = optimization_profile.get("weak_agents", [])

        for agent in weak_agents:

            governance["unstable_agents"].append(agent.get("agent"))

        # =====================================================
        # 🔥 GOVERNANCE SCORE
        # =====================================================

        score = 1.0

        if governance["constitutional_overreach_risk"]:
            score -= 0.20

        if governance["semantic_drift_risk"]:
            score -= 0.25

        if governance["requires_human_review"]:
            score -= 0.15

        governance["governance_score"] = round(max(score, 0.0), 2)

    except Exception as e:

        print("❌ GOVERNANCE ENGINE ERROR:")

        print(str(e))

    return governance
