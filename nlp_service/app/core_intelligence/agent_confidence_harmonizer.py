# =========================================================
# 🔥 AGENT CONFIDENCE HARMONIZER
# =========================================================

def harmonize_agent_confidence(agent_outputs):

    harmonized_output = {

        "dominant_agent": None,

        "dominant_confidence": 0.0,

        "confidence_ranking": [],

        "requires_arbitration": False,

        "confidence_spread": 0.0,

        "semantic_consensus_strength": 0.0
    }

    try:

        confidence_scores = []

        # =====================================================
        # 🔥 EXTRACT CONFIDENCES
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
                            output.get(
                                "constitutional_escalation_score",
                                0.50
                            )
                        )
                    )
                )

            confidence_scores.append({

                "agent":
                    agent_name,

                "confidence":
                    round(float(confidence), 2)
            })

        # =====================================================
        # 🔥 SORT CONFIDENCES
        # =====================================================

        confidence_scores = sorted(

            confidence_scores,

            key=lambda x: x["confidence"],

            reverse=True
        )

        harmonized_output[
            "confidence_ranking"
        ] = confidence_scores

        # =====================================================
        # 🔥 DOMINANT AGENT
        # =====================================================

        if confidence_scores:

            harmonized_output[
                "dominant_agent"
            ] = confidence_scores[0]["agent"]

            harmonized_output[
                "dominant_confidence"
            ] = confidence_scores[0]["confidence"]

        # =====================================================
        # 🔥 CONFIDENCE SPREAD
        # =====================================================

        if len(confidence_scores) >= 2:

            spread = abs(

                confidence_scores[0]["confidence"]
                -
                confidence_scores[-1]["confidence"]
            )

            harmonized_output[
                "confidence_spread"
            ] = round(spread, 2)

            if spread > 0.40:

                harmonized_output[
                    "requires_arbitration"
                ] = True

        # =====================================================
        # 🔥 SEMANTIC CONSENSUS
        # =====================================================

        if confidence_scores:

            avg_confidence = sum(

                x["confidence"]
                for x in confidence_scores

            ) / len(confidence_scores)

            harmonized_output[
                "semantic_consensus_strength"
            ] = round(avg_confidence, 2)

    except Exception as e:

        print(
            "❌ AGENT HARMONIZATION ERROR:"
        )

        print(str(e))

    return harmonized_output
