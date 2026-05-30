# =========================================================
# 🔥 LEGAL COGNITION OPTIMIZATION ENGINE
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 OPTIMIZATION STORE
# =========================================================

COGNITION_OPTIMIZATION = {
    "agent_scores": defaultdict(float),
    "agent_success_counts": defaultdict(int),
    "agent_failure_counts": defaultdict(int),
    "routing_efficiency": defaultdict(list),
    "semantic_resolution_scores": [],
}

# =========================================================
# 🔥 UPDATE AGENT PERFORMANCE
# =========================================================


def update_agent_performance(agent_name, success=True, confidence=0.50):

    try:

        if success:

            COGNITION_OPTIMIZATION["agent_success_counts"][agent_name] += 1

            COGNITION_OPTIMIZATION["agent_scores"][agent_name] += confidence

        else:

            COGNITION_OPTIMIZATION["agent_failure_counts"][agent_name] += 1

            COGNITION_OPTIMIZATION["agent_scores"][agent_name] -= 0.25

        return True

    except Exception as e:

        print("❌ AGENT PERFORMANCE UPDATE ERROR:")

        print(str(e))

        return False


# =========================================================
# 🔥 UPDATE ROUTING EFFICIENCY
# =========================================================


def update_routing_efficiency(routing_mode, efficiency_score):

    try:

        COGNITION_OPTIMIZATION["routing_efficiency"][routing_mode].append(
            efficiency_score
        )

        return True

    except Exception as e:

        print("❌ ROUTING EFFICIENCY ERROR:")

        print(str(e))

        return False


# =========================================================
# 🔥 UPDATE RESOLUTION QUALITY
# =========================================================


def update_semantic_resolution(resolution_strength):

    try:

        COGNITION_OPTIMIZATION["semantic_resolution_scores"].append(resolution_strength)

        return True

    except Exception as e:

        print("❌ RESOLUTION UPDATE ERROR:")

        print(str(e))

        return False


# =========================================================
# 🔥 BUILD OPTIMIZATION PROFILE
# =========================================================


def build_optimization_profile():

    profile = {
        "top_agents": [],
        "weak_agents": [],
        "average_resolution_strength": 0.0,
        "routing_modes": {},
        "system_stability": 0.0,
    }

    try:

        # =====================================================
        # 🔥 AGENT RANKING
        # =====================================================

        scores = []

        for agent, score in COGNITION_OPTIMIZATION["agent_scores"].items():

            scores.append({"agent": agent, "score": round(score, 2)})

        scores = sorted(scores, key=lambda x: x["score"], reverse=True)

        profile["top_agents"] = scores[:5]

        profile["weak_agents"] = [x for x in scores if x["score"] < 0]

        # =====================================================
        # 🔥 RESOLUTION STRENGTH
        # =====================================================

        resolutions = COGNITION_OPTIMIZATION["semantic_resolution_scores"]

        if resolutions:

            avg_resolution = sum(resolutions) / len(resolutions)

            profile["average_resolution_strength"] = round(avg_resolution, 2)

        # =====================================================
        # 🔥 ROUTING MODES
        # =====================================================

        for mode, values in COGNITION_OPTIMIZATION["routing_efficiency"].items():

            if values:

                profile["routing_modes"][mode] = round(sum(values) / len(values), 2)

        # =====================================================
        # 🔥 SYSTEM STABILITY
        # =====================================================

        stability = min(profile["average_resolution_strength"] * 1.2, 1.0)

        profile["system_stability"] = round(stability, 2)

    except Exception as e:

        print("❌ OPTIMIZATION PROFILE ERROR:")

        print(str(e))

    return profile
