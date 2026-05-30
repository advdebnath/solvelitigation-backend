# =========================================================
# 🔥 SEMANTIC DISPATCH ENGINE
# =========================================================

from app.core_intelligence.agent_registry import get_agent

# =========================================================
# 🔥 SEMANTIC DISPATCH ENGINE
# =========================================================


def semantic_dispatch(
    semantic_confidence=0.5,
    contradiction_risk_score=0.5,
    constitutional_weight=0.5,
    precedent_density=0.5,
    procedural_complexity=0.5,
    doctrinal_density=0.5,
):

    dispatch_plan = []

    # =====================================================
    # 🔥 VALIDATION DISPATCH
    # =====================================================

    if semantic_confidence < 0.70:

        dispatch_plan.append("validation")

    # =====================================================
    # 🔥 EVIDENTIARY DISPATCH
    # =====================================================

    if contradiction_risk_score > 0.40:

        dispatch_plan.append("evidentiary")

    # =====================================================
    # 🔥 STRATEGIC DISPATCH
    # =====================================================

    if constitutional_weight > 0.60:

        dispatch_plan.append("strategy")

    # =====================================================
    # 🔥 PROCEDURAL DISPATCH
    # =====================================================

    if procedural_complexity > 0.50:

        dispatch_plan.append("procedural")

    # =====================================================
    # 🔥 GRAPH DISPATCH
    # =====================================================

    if doctrinal_density > 0.50:

        dispatch_plan.append("semantic_graph")

    # =====================================================
    # 🔥 RAG DISPATCH
    # =====================================================

    if precedent_density > 0.50:

        dispatch_plan.append("rag")

    # =====================================================
    # 🔥 AGENTIC DISPATCH
    # =====================================================

    if constitutional_weight > 0.75 or precedent_density > 0.75:

        dispatch_plan.append("agentic")

    # =====================================================
    # 🔥 REMOVE DUPLICATES
    # =====================================================

    dispatch_plan = list(dict.fromkeys(dispatch_plan))

    return dispatch_plan


# =========================================================
# 🔥 DYNAMIC AGENT FETCHER
# =========================================================


def resolve_agents(dispatch_plan):

    resolved_agents = {}

    for agent_name in dispatch_plan:

        agent = get_agent(agent_name)

        if agent:

            resolved_agents[agent_name] = agent

    return resolved_agents
