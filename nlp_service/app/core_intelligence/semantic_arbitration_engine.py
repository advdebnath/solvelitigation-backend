# =========================================================
# 🔥 SEMANTIC ARBITRATION ENGINE
# =========================================================


def arbitrate_semantic_conflicts(harmonized_output, agent_outputs):

    arbitration_result = {
        "final_authoritative_agent": None,
        "arbitration_required": False,
        "suppressed_agents": [],
        "preferred_reasoning_path": None,
        "constitutional_priority_applied": False,
        "semantic_resolution_strength": 0.0,
    }

    try:

        dominant_agent = harmonized_output.get("dominant_agent")

        confidence_spread = harmonized_output.get("confidence_spread", 0.0)

        arbitration_required = harmonized_output.get("requires_arbitration", False)

        arbitration_result["arbitration_required"] = arbitration_required

        # =====================================================
        # 🔥 DEFAULT DOMINANT AGENT
        # =====================================================

        arbitration_result["final_authoritative_agent"] = dominant_agent

        arbitration_result["preferred_reasoning_path"] = dominant_agent

        # =====================================================
        # 🔥 CONSTITUTIONAL PRIORITY
        # =====================================================

        if "strategy" in agent_outputs:

            strategy_output = agent_outputs.get("strategy", {})

            constitutional_score = strategy_output.get(
                "constitutional_escalation_score", 0.0
            )

            if constitutional_score >= 0.80:

                arbitration_result["final_authoritative_agent"] = "strategy"

                arbitration_result["preferred_reasoning_path"] = (
                    "constitutional_supremacy"
                )

                arbitration_result["constitutional_priority_applied"] = True

        # =====================================================
        # 🔥 SUPPRESS LOW CONFIDENCE AGENTS
        # =====================================================

        for agent_name, output in agent_outputs.items():

            confidence = 0.50

            if isinstance(output, dict):

                confidence = output.get(
                    "confidence",
                    output.get(
                        "agentic_confidence",
                        output.get(
                            "semantic_support_score",
                            output.get("constitutional_escalation_score", 0.50),
                        ),
                    ),
                )

            if confidence < 0.45:

                arbitration_result["suppressed_agents"].append(agent_name)

        # =====================================================
        # 🔥 RESOLUTION STRENGTH
        # =====================================================

        resolution_strength = 1.0 - min(confidence_spread, 1.0)

        arbitration_result["semantic_resolution_strength"] = round(
            resolution_strength, 2
        )

    except Exception as e:

        print("❌ SEMANTIC ARBITRATION ERROR:")

        print(str(e))

    return arbitration_result
