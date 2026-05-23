# =========================================================
# 🔥 SOVEREIGN DOCTRINE EXCHANGE GATEWAY
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 GATEWAY STATE
# =========================================================

DOCTRINE_GATEWAY = {

    "exchange_treaties": [],

    "trust_scores": defaultdict(float),

    "gateway_events": [],

    "compatibility_matrix": [],

    "gateway_mode": "REGULATED_EXCHANGE"
}

# =========================================================
# 🔥 REGISTER EXCHANGE TREATY
# =========================================================

def register_exchange_treaty(

    source_federation,
    target_federation,
    doctrine_type,
    trust_level=0.50
):

    treaty = {

        "source":
            source_federation,

        "target":
            target_federation,

        "doctrine":
            doctrine_type,

        "trust_level":
            round(trust_level, 2),

        "status":
            "ACTIVE"
    }

    DOCTRINE_GATEWAY[
        "exchange_treaties"
    ].append(treaty)

    treaty_key = (
        f"{source_federation}->{target_federation}"
    )

    DOCTRINE_GATEWAY[
        "trust_scores"
    ][treaty_key] = round(
        trust_level,
        2
    )

    return True

# =========================================================
# 🔥 VALIDATE COMPATIBILITY
# =========================================================

def validate_doctrine_compatibility(

    source_federation,
    target_federation,
    doctrine_weight_a,
    doctrine_weight_b
):

    compatibility_score = round(

        1 - abs(
            doctrine_weight_a
            -
            doctrine_weight_b
        ),

        2
    )

    compatible = compatibility_score >= 0.60

    result = {

        "source":
            source_federation,

        "target":
            target_federation,

        "compatibility_score":
            compatibility_score,

        "compatible":
            compatible
    }

    DOCTRINE_GATEWAY[
        "compatibility_matrix"
    ].append(result)

    return result

# =========================================================
# 🔥 EXECUTE DOCTRINE EXCHANGE
# =========================================================

def execute_doctrine_exchange(

    source_federation,
    target_federation,
    doctrine_name
):

    treaty_key = (
        f"{source_federation}->{target_federation}"
    )

    trust_score = DOCTRINE_GATEWAY[
        "trust_scores"
    ].get(
        treaty_key,
        0.0
    )

    if trust_score < 0.40:

        return {

            "exchange_allowed": False,

            "reason":
                "LOW_TRUST_SCORE"
        }

    exchange_event = {

        "source":
            source_federation,

        "target":
            target_federation,

        "doctrine":
            doctrine_name,

        "trust_score":
            trust_score,

        "status":
            "EXCHANGED"
    }

    DOCTRINE_GATEWAY[
        "gateway_events"
    ].append(exchange_event)

    return {

        "exchange_allowed": True,

        "event":
            exchange_event
    }

# =========================================================
# 🔥 FETCH GATEWAY STATE
# =========================================================

def get_doctrine_gateway_state():

    return DOCTRINE_GATEWAY
