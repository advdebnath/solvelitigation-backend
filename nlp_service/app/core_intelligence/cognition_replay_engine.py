# =========================================================
# 🔥 COGNITION REPLAY ENGINE
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 BUILD REPLAY TIMELINE
# =========================================================

def build_cognition_replay(

    telemetry_events
):

    replay = {

        "timeline": [],

        "agent_sequence": [],

        "event_summary": defaultdict(int),

        "constitutional_escalations": [],

        "contradiction_events": [],

        "semantic_execution_flow": []
    }

    try:

        sorted_events = sorted(

            telemetry_events,

            key=lambda x: x.get(
                "timestamp",
                ""
            )
        )

        for event in sorted_events:

            agent = event.get(
                "agent"
            )

            event_type = event.get(
                "event_type"
            )

            payload = event.get(
                "payload",
                {}
            )

            replay["timeline"].append({

                "agent":
                    agent,

                "event":
                    event_type,

                "payload":
                    payload
            })

            replay["agent_sequence"].append(
                agent
            )

            replay["event_summary"][
                event_type
            ] += 1

            replay[
                "semantic_execution_flow"
            ].append(

                f"{agent} -> {event_type}"
            )

            # =================================================
            # 🔥 CONSTITUTIONAL EVENTS
            # =================================================

            if "constitutional" in event_type.lower():

                replay[
                    "constitutional_escalations"
                ].append(event)

            # =================================================
            # 🔥 CONTRADICTION EVENTS
            # =================================================

            if "contradiction" in event_type.lower():

                replay[
                    "contradiction_events"
                ].append(event)

        # =====================================================
        # 🔥 REMOVE DUPLICATES
        # =====================================================

        replay["agent_sequence"] = list(
            dict.fromkeys(
                replay["agent_sequence"]
            )
        )

        replay["event_summary"] = dict(
            replay["event_summary"]
        )

    except Exception as e:

        print(
            "❌ COGNITION REPLAY ERROR:"
        )

        print(str(e))

    return replay
