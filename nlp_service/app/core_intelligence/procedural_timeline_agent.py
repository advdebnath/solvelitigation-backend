# =========================================================
# 🔥 PROCEDURAL TIMELINE INTELLIGENCE AGENT
# =========================================================

def run_procedural_timeline_analysis(

    reconstructed_text,
    constitutional_weight,
    semantic_confidence
):

    procedural_timeline = {

        "estimated_duration_months": 24,

        "delay_risk": "MODERATE",

        "urgency_score": 0.50,

        "appellate_delay_probability": 0.50,

        "procedural_bottlenecks": [],

        "time_sensitive_relief_probability":
            0.50
    }

    try:

        upper_text = reconstructed_text.upper()

        procedural_terms = [

            "ADJOURNMENT",
            "REMAND",
            "INTERIM ORDER",
            "NOTICE ISSUED",
            "MULTIPLE APPEALS",
            "LONG PENDENCY"
        ]

        urgency_terms = [

            "URGENT",
            "BAIL",
            "HABEAS CORPUS",
            "STAY APPLICATION",
            "INTERIM RELIEF",
            "STATUS QUO"
        ]

        procedural_hits = sum(
            1 for t in procedural_terms
            if t in upper_text
        )

        urgency_hits = sum(
            1 for t in urgency_terms
            if t in upper_text
        )

        urgency_score = round(
            min(
                1.0,
                urgency_hits / 5
            ),
            2
        )

        appellate_delay_probability = round(
            min(
                1.0,
                procedural_hits / 5
            ),
            2
        )

        estimated_duration_months = (
            12 + (procedural_hits * 6)
        )

        procedural_bottlenecks = []

        if procedural_hits >= 2:

            procedural_bottlenecks.append(
                "MULTI_STAGE_LITIGATION"
            )

        if "REMAND" in upper_text:

            procedural_bottlenecks.append(
                "REMAND_DELAY"
            )

        if "MULTIPLE APPEALS" in upper_text:

            procedural_bottlenecks.append(
                "APPELLATE_ESCALATION"
            )

        delay_risk = "MODERATE"

        if appellate_delay_probability >= 0.7:

            delay_risk = "HIGH"

        elif urgency_score >= 0.8:

            delay_risk = "LOW"

        time_sensitive_relief_probability = round(
            (
                urgency_score +
                constitutional_weight +
                semantic_confidence
            ) / 3,
            2
        )

        procedural_timeline.update({

            "estimated_duration_months":
                estimated_duration_months,

            "delay_risk":
                delay_risk,

            "urgency_score":
                urgency_score,

            "appellate_delay_probability":
                appellate_delay_probability,

            "procedural_bottlenecks":
                procedural_bottlenecks,

            "time_sensitive_relief_probability":
                time_sensitive_relief_probability
        })

    except Exception as e:

        print(
            "❌ PROCEDURAL TIMELINE AGENT ERROR:"
        )

        print(str(e))

    return procedural_timeline
