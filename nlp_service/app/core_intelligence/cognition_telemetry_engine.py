# =========================================================
# 🔥 COGNITION TELEMETRY ENGINE
# =========================================================

from datetime import datetime

# =========================================================
# 🔥 GLOBAL TELEMETRY STORE
# =========================================================

COGNITION_TELEMETRY = []

# =========================================================
# 🔥 RECORD TELEMETRY
# =========================================================


def record_telemetry(agent_name, event_type, payload=None):

    telemetry_event = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent": agent_name,
        "event_type": event_type,
        "payload": payload or {},
    }

    COGNITION_TELEMETRY.append(telemetry_event)

    return telemetry_event


# =========================================================
# 🔥 FETCH TELEMETRY
# =========================================================


def get_telemetry():

    return COGNITION_TELEMETRY


# =========================================================
# 🔥 FILTER BY AGENT
# =========================================================


def get_agent_telemetry(agent_name):

    return [item for item in COGNITION_TELEMETRY if item["agent"] == agent_name]


# =========================================================
# 🔥 CLEAR TELEMETRY
# =========================================================


def clear_telemetry():

    COGNITION_TELEMETRY.clear()

    return True
