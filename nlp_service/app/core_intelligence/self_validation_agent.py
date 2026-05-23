# =========================================================
# 🔥 SELF VALIDATION AGENT
# =========================================================

def run_self_validation(

    adaptive_reasoning,
    semantic_outcome_prediction,
    historical_consistency_score,
    constitutional_consistency
):

    self_validation = {

        "reasoning_consistency_score": 0.50,

        "prediction_alignment_score": 0.50,

        "doctrine_prediction_conflict": False,

        "strategic_reliability": "MODERATE",

        "semantic_confidence": 0.50
    }

    try:

        constitutional_weight_value = (
            adaptive_reasoning.get(
                "constitutional_weight",
                0.5
            )
        )

        persuasive_force_value = (
            adaptive_reasoning.get(
                "persuasive_force_score",
                0.5
            )
        )

        outcome_confidence_value = (
            semantic_outcome_prediction.get(
                "outcome_confidence",
                0.5
            )
        )

        litigation_risk_value = (
            semantic_outcome_prediction.get(
                "litigation_risk_score",
                0.5
            )
        )

        reasoning_consistency_score = round(
            (
                constitutional_weight_value +
                persuasive_force_value +
                historical_consistency_score
            ) / 3,
            2
        )

        prediction_alignment_score = round(
            max(
                0.0,
                1 - abs(
                    persuasive_force_value -
                    outcome_confidence_value
                )
            ),
            2
        )

        doctrine_prediction_conflict = False

        if (
            constitutional_weight_value >= 0.7
            and litigation_risk_value >= 0.7
        ):

            doctrine_prediction_conflict = True

        semantic_confidence = round(
            (
                reasoning_consistency_score +
                prediction_alignment_score +
                constitutional_consistency
            ) / 3,
            2
        )

        strategic_reliability = "MODERATE"

        if semantic_confidence >= 0.8:

            strategic_reliability = "HIGH"

        elif semantic_confidence <= 0.4:

            strategic_reliability = "LOW"

        self_validation.update({

            "reasoning_consistency_score":
                reasoning_consistency_score,

            "prediction_alignment_score":
                prediction_alignment_score,

            "doctrine_prediction_conflict":
                doctrine_prediction_conflict,

            "strategic_reliability":
                strategic_reliability,

            "semantic_confidence":
                semantic_confidence
        })

    except Exception as e:

        print("❌ SELF VALIDATION AGENT ERROR:")
        print(str(e))

    return self_validation
