# =========================================================
# 🔥 JURISPRUDENTIAL EVOLUTION ENGINE
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 EVOLUTION ANALYSIS
# =========================================================

def analyze_jurisprudential_evolution(

    memory_summary,
    constitutional_memory,
    precedent_memory
):

    evolution = {

        "dominant_doctrines": [],

        "constitutional_growth_index": 0.0,

        "precedent_reinforcement_strength": 0.0,

        "jurisprudential_shift_detected": False,

        "emerging_clusters": [],

        "adaptive_weight_updates": {}
    }

    try:

        # =====================================================
        # 🔥 CONSTITUTIONAL GROWTH
        # =====================================================

        constitutional_events = len(
            constitutional_memory
        )

        precedent_events = len(
            precedent_memory
        )

        total_events = max(
            constitutional_events + precedent_events,
            1
        )

        constitutional_growth = (
            constitutional_events / total_events
        )

        evolution[
            "constitutional_growth_index"
        ] = round(
            constitutional_growth,
            2
        )

        # =====================================================
        # 🔥 PRECEDENT REINFORCEMENT
        # =====================================================

        reinforcement = min(
            precedent_events / 10,
            1.0
        )

        evolution[
            "precedent_reinforcement_strength"
        ] = round(
            reinforcement,
            2
        )

        # =====================================================
        # 🔥 DOCTRINAL ANALYSIS
        # =====================================================

        doctrine_counter = defaultdict(int)

        for event in constitutional_memory:

            article = event.get(
                "article",
                "UNKNOWN"
            )

            doctrine_counter[
                article
            ] += 1

        dominant = sorted(

            doctrine_counter.items(),

            key=lambda x: x[1],

            reverse=True
        )

        evolution[
            "dominant_doctrines"
        ] = dominant[:5]

        # =====================================================
        # 🔥 SHIFT DETECTION
        # =====================================================

        if constitutional_growth >= 0.70:

            evolution[
                "jurisprudential_shift_detected"
            ] = True

            evolution[
                "emerging_clusters"
            ].append(
                "constitutional_expansion"
            )

        if reinforcement >= 0.80:

            evolution[
                "emerging_clusters"
            ].append(
                "precedent_stabilization"
            )

        # =====================================================
        # 🔥 ADAPTIVE WEIGHTING
        # =====================================================

        evolution[
            "adaptive_weight_updates"
        ] = {

            "constitutional_priority":
                round(
                    constitutional_growth * 1.5,
                    2
                ),

            "precedent_priority":
                round(
                    reinforcement * 1.3,
                    2
                )
        }

    except Exception as e:

        print(
            "❌ JURISPRUDENTIAL EVOLUTION ERROR:"
        )

        print(str(e))

    return evolution
