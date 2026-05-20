# =========================================================
# 🔥 TEMPORAL LEGAL ANALYTICS ENGINE
# =========================================================

from collections import defaultdict


def generate_temporal_legal_analytics(
    doctrine_data_list
):

    """
    Generate doctrine evolution timelines.
    """

    try:

        temporal_map = defaultdict(list)

        # =====================================================
        # 🔥 INPUT SAFETY
        # =====================================================

        if not isinstance(
            doctrine_data_list,
            list
        ):

            return {
                "temporal_analysis": {},
                "confidence": 40
            }

        # =====================================================
        # 🔥 PROCESS DOCTRINES
        # =====================================================

        for item in doctrine_data_list:

            # =================================================
            # 🔥 STRING NORMALIZATION
            # =================================================

            if isinstance(item, str):

                item = {
                    "doctrine": item,
                    "timeline": []
                }

            if not isinstance(item, dict):
                continue

            doctrine = item.get(
                "doctrine",
                "unknown"
            )

            timeline = item.get(
                "timeline",
                []
            )

            # =================================================
            # 🔥 TIMELINE SAFETY
            # =================================================

            if isinstance(timeline, str):

                timeline = [{
                    "year": None,
                    "principle": timeline
                }]

            if not isinstance(timeline, list):
                continue

            # =================================================
            # 🔥 PROCESS ENTRIES
            # =================================================

            for entry in timeline:

                # =============================================
                # 🔥 STRING ENTRY SAFETY
                # =============================================

                if isinstance(entry, str):

                    entry = {
                        "year": None,
                        "principle": entry
                    }

                if not isinstance(entry, dict):
                    continue

                year = entry.get(
                    "year",
                    None
                )

                principle = entry.get(
                    "principle",
                    ""
                )

                temporal_map[doctrine].append({

                    "year": year,

                    "principle": principle
                })

        # =====================================================
        # 🔥 SORT
        # =====================================================

        for doctrine in temporal_map:

            temporal_map[doctrine] = sorted(

                temporal_map[doctrine],

                key=lambda x:
                    x.get("year") or 0
            )

        # =====================================================
        # 🔥 RESPONSE
        # =====================================================

        return {

            "temporal_analysis":
                dict(temporal_map),

            "confidence":
                95
        }

    except Exception as e:

        print(
            "❌ Temporal Analytics Error:"
        )

        print(e)

        return {

            "temporal_analysis": {},

            "confidence": 40
        }
