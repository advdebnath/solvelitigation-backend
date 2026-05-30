# =========================================================
# 🔥 DISTRIBUTED SEMANTIC FEDERATION ENGINE
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 FEDERATION STATE
# =========================================================

SEMANTIC_FEDERATION = {
    "federations": {},
    "jurisdiction_clusters": defaultdict(list),
    "federation_routes": [],
    "federation_health": {},
    "federation_mode": "GLOBAL_ACTIVE",
}

# =========================================================
# 🔥 REGISTER FEDERATION
# =========================================================


def register_federation(federation_name, jurisdiction):

    SEMANTIC_FEDERATION["federations"][federation_name] = {
        "jurisdiction": jurisdiction,
        "status": "ACTIVE",
    }

    SEMANTIC_FEDERATION["jurisdiction_clusters"][jurisdiction].append(federation_name)

    SEMANTIC_FEDERATION["federation_health"][federation_name] = 1.0

    return True


# =========================================================
# 🔥 UPDATE FEDERATION HEALTH
# =========================================================


def update_federation_health(federation_name, health_score):

    SEMANTIC_FEDERATION["federation_health"][federation_name] = round(health_score, 2)

    if health_score < 0.40:

        SEMANTIC_FEDERATION["federations"][federation_name]["status"] = "DEGRADED"

    return True


# =========================================================
# 🔥 REGISTER FEDERATION ROUTE
# =========================================================


def register_federation_route(source_federation, target_federation, doctrine_type):

    SEMANTIC_FEDERATION["federation_routes"].append(
        {
            "source": source_federation,
            "target": target_federation,
            "doctrine": doctrine_type,
        }
    )

    return True


# =========================================================
# 🔥 FETCH HEALTHY FEDERATIONS
# =========================================================


def get_healthy_federations():

    healthy = []

    for federation, health in SEMANTIC_FEDERATION["federation_health"].items():

        if health >= 0.60:

            healthy.append(federation)

    return healthy


# =========================================================
# 🔥 FETCH FEDERATION STATE
# =========================================================


def get_federation_state():

    return SEMANTIC_FEDERATION
