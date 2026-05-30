# =========================================================
# 🔥 AUTONOMOUS LEGAL STRATEGY ORCHESTRATION AGENT
# =========================================================


def run_strategy_orchestration(
    adaptive_reasoning,
    procedural_timeline,
    semantic_graph_intelligence,
    rag_reasoning,
    agentic_reasoning,
):

    strategy_orchestration = {
        "primary_strategy": "STANDARD_LITIGATION",
        "fallback_strategy": "REVIEW_OR_APPEAL",
        "recommended_forum": "HIGH_COURT",
        "appeal_pathway": [],
        "constitutional_escalation_score": 0.50,
        "strategic_sequence": [],
    }

    try:

        constitutional_weight = adaptive_reasoning.get("constitutional_weight", 0.5)

        delay_risk = procedural_timeline.get("delay_risk", "MODERATE")

        semantic_cluster = semantic_graph_intelligence.get(
            "semantic_cluster", "GENERAL_DOCTRINE"
        )

        doctrine_alignment = rag_reasoning.get("doctrine_alignment", 0.5)

        agentic_confidence = agentic_reasoning.get("agentic_confidence", 0.5)

        constitutional_escalation_score = round(
            (constitutional_weight + doctrine_alignment + agentic_confidence) / 3, 2
        )

        strategic_sequence = [
            "FACTUAL_CONSOLIDATION",
            "PRECEDENT_RESEARCH",
            "CONSTITUTIONAL_ANALYSIS",
            "PRIMARY_ARGUMENT_PREPARATION",
            "FORUM_SELECTION",
            "REMEDY_OPTIMIZATION",
        ]

        appeal_pathway = ["TRIAL_FORUM", "APPELLATE_FORUM", "CONSTITUTIONAL_REMEDY"]

        recommended_forum = "HIGH_COURT"

        if constitutional_escalation_score >= 0.75:

            recommended_forum = "SUPREME_COURT"

        if semantic_cluster == "DETENTION_CLUSTER":

            strategic_sequence.append("URGENT_LIBERTY_MENTIONING")

        primary_strategy = "STANDARD_LITIGATION"

        if delay_risk == "HIGH":

            primary_strategy = "EXPEDITED_REMEDY"

        fallback_strategy = "REVIEW_OR_APPEAL"

        if constitutional_escalation_score >= 0.80:

            fallback_strategy = "CONSTITUTIONAL_CHALLENGE"

        strategy_orchestration.update(
            {
                "primary_strategy": primary_strategy,
                "fallback_strategy": fallback_strategy,
                "recommended_forum": recommended_forum,
                "appeal_pathway": appeal_pathway,
                "constitutional_escalation_score": constitutional_escalation_score,
                "strategic_sequence": strategic_sequence,
            }
        )

    except Exception as e:

        print("❌ STRATEGY ORCHESTRATION AGENT ERROR:")

        print(str(e))

    return strategy_orchestration
