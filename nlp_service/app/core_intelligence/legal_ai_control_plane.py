# =========================================================
# 🔥 ENTERPRISE LEGAL AI CONTROL PLANE
# =========================================================

from datetime import datetime

# =========================================================
# 🔥 GLOBAL CONTROL STATE
# =========================================================

CONTROL_PLANE_STATE = {

    "system_mode": "ACTIVE",

    "governance_override": False,

    "emergency_shutdown": False,

    "cognition_load_level": "NORMAL",

    "active_agents": [],

    "last_governance_check": None,

    "system_health_score": 1.0
}

# =========================================================
# 🔥 UPDATE SYSTEM MODE
# =========================================================

def update_system_mode(mode):

    CONTROL_PLANE_STATE[
        "system_mode"
    ] = mode

    return CONTROL_PLANE_STATE

# =========================================================
# 🔥 REGISTER ACTIVE AGENT
# =========================================================

def register_active_agent(agent_name):

    if agent_name not in CONTROL_PLANE_STATE[
        "active_agents"
    ]:

        CONTROL_PLANE_STATE[
            "active_agents"
        ].append(agent_name)

    return CONTROL_PLANE_STATE[
        "active_agents"
    ]

# =========================================================
# 🔥 CLEAR ACTIVE AGENTS
# =========================================================

def clear_active_agents():

    CONTROL_PLANE_STATE[
        "active_agents"
    ] = []

    return True

# =========================================================
# 🔥 GOVERNANCE OVERRIDE
# =========================================================

def activate_governance_override():

    CONTROL_PLANE_STATE[
        "governance_override"
    ] = True

    return True

# =========================================================
# 🔥 EMERGENCY SHUTDOWN
# =========================================================

def activate_emergency_shutdown():

    CONTROL_PLANE_STATE[
        "emergency_shutdown"
    ] = True

    CONTROL_PLANE_STATE[
        "system_mode"
    ] = "SAFE_MODE"

    return True

# =========================================================
# 🔥 UPDATE SYSTEM HEALTH
# =========================================================

def update_system_health(score):

    CONTROL_PLANE_STATE[
        "system_health_score"
    ] = round(score, 2)

    CONTROL_PLANE_STATE[
        "last_governance_check"
    ] = datetime.utcnow().isoformat()

    # =====================================================
    # 🔥 AUTO SAFE MODE
    # =====================================================

    if score < 0.40:

        CONTROL_PLANE_STATE[
            "system_mode"
        ] = "SAFE_MODE"

    elif score < 0.70:

        CONTROL_PLANE_STATE[
            "cognition_load_level"
        ] = "ELEVATED"

    else:

        CONTROL_PLANE_STATE[
            "cognition_load_level"
        ] = "NORMAL"

    return CONTROL_PLANE_STATE

# =========================================================
# 🔥 FETCH CONTROL STATE
# =========================================================

def get_control_plane_state():

    return CONTROL_PLANE_STATE
