# =========================================================
# 🔥 COGNITION TELEMETRY MODEL
# =========================================================

from datetime import datetime

# =========================================================
# 🔥 BUILD TELEMETRY DOCUMENT
# =========================================================

def build_telemetry_document(

    agent_name,
    event_type,
    payload=None
):

    return {

        "agent":
            agent_name,

        "event_type":
            event_type,

        "payload":
            payload or {},

        "created_at":
            datetime.utcnow()
    }
