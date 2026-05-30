# =========================================================
# 🔥 SOVEREIGN LEGAL AI ISOLATION ENGINE
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 ISOLATION STATE
# =========================================================

SOVEREIGN_ISOLATION = {
    "isolated_federations": {},
    "allowed_bridges": [],
    "blocked_routes": [],
    "jurisdiction_policies": defaultdict(dict),
    "isolation_mode": "SOVEREIGN_ACTIVE",
}

# =========================================================
# 🔥 REGISTER ISOLATED FEDERATION
# =========================================================


def register_isolated_federation(
    federation_name, jurisdiction, isolation_level="STRICT"
):

    SOVEREIGN_ISOLATION["isolated_federations"][federation_name] = {
        "jurisdiction": jurisdiction,
        "isolation_level": isolation_level,
        "status": "ISOLATED",
    }

    return True


# =========================================================
# 🔥 ALLOW DOCTRINE BRIDGE
# =========================================================


def allow_doctrine_bridge(source_federation, target_federation, doctrine_type):

    SOVEREIGN_ISOLATION["allowed_bridges"].append(
        {
            "source": source_federation,
            "target": target_federation,
            "doctrine": doctrine_type,
            "status": "ALLOWED",
        }
    )

    return True


# =========================================================
# 🔥 BLOCK ROUTE
# =========================================================


def block_federation_route(source_federation, target_federation, reason):

    SOVEREIGN_ISOLATION["blocked_routes"].append(
        {
            "source": source_federation,
            "target": target_federation,
            "reason": reason,
            "status": "BLOCKED",
        }
    )

    return True


# =========================================================
# 🔥 SET JURISDICTION POLICY
# =========================================================


def set_jurisdiction_policy(jurisdiction, policy_name, policy_value):

    SOVEREIGN_ISOLATION["jurisdiction_policies"][jurisdiction][
        policy_name
    ] = policy_value

    return True


# =========================================================
# 🔥 VALIDATE FEDERATION ACCESS
# =========================================================


def validate_federation_access(source_federation, target_federation):

    for blocked in SOVEREIGN_ISOLATION["blocked_routes"]:

        if (
            blocked["source"] == source_federation
            and blocked["target"] == target_federation
        ):

            return {"access_allowed": False, "reason": blocked["reason"]}

    return {"access_allowed": True, "reason": "AUTHORIZED"}


# =========================================================
# 🔥 FETCH ISOLATION STATE
# =========================================================


def get_sovereign_isolation_state():

    return SOVEREIGN_ISOLATION
