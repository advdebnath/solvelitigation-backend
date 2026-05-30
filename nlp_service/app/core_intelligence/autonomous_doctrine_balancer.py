# =========================================================
# 🔥 AUTONOMOUS DOCTRINE BALANCER
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 GLOBAL DOCTRINAL STATE
# =========================================================

DOCTRINAL_BALANCE = {
    "federation_doctrines": defaultdict(dict),
    "conflict_matrix": [],
    "equilibrium_state": "STABLE",
    "balancing_events": [],
    "constitutional_priority_index": 1.0,
}

# =========================================================
# 🔥 REGISTER DOCTRINE
# =========================================================


def register_doctrine(federation_name, doctrine_name, doctrine_weight):

    DOCTRINAL_BALANCE["federation_doctrines"][federation_name][doctrine_name] = round(
        doctrine_weight, 2
    )

    return True


# =========================================================
# 🔥 DETECT DOCTRINAL CONFLICTS
# =========================================================


def detect_doctrinal_conflicts():

    conflicts = []

    try:

        federations = DOCTRINAL_BALANCE["federation_doctrines"]

        federation_names = list(federations.keys())

        for i in range(len(federation_names)):

            for j in range(i + 1, len(federation_names)):

                fed_a = federation_names[i]
                fed_b = federation_names[j]

                doctrines_a = federations[fed_a]
                doctrines_b = federations[fed_b]

                for doctrine in doctrines_a:

                    if doctrine in doctrines_b:

                        weight_diff = abs(doctrines_a[doctrine] - doctrines_b[doctrine])

                        if weight_diff >= 0.40:

                            conflicts.append(
                                {
                                    "doctrine": doctrine,
                                    "federation_a": fed_a,
                                    "federation_b": fed_b,
                                    "weight_difference": round(weight_diff, 2),
                                }
                            )

        DOCTRINAL_BALANCE["conflict_matrix"] = conflicts

        if conflicts:

            DOCTRINAL_BALANCE["equilibrium_state"] = "UNSTABLE"

    except Exception as e:

        print("❌ DOCTRINAL CONFLICT ERROR:")

        print(str(e))

    return conflicts


# =========================================================
# 🔥 BALANCE DOCTRINES
# =========================================================


def balance_doctrines():

    balancing_actions = []

    try:

        conflicts = DOCTRINAL_BALANCE["conflict_matrix"]

        for conflict in conflicts:

            doctrine = conflict["doctrine"]

            fed_a = conflict["federation_a"]
            fed_b = conflict["federation_b"]

            doctrines = DOCTRINAL_BALANCE["federation_doctrines"]

            avg_weight = round(
                (doctrines[fed_a][doctrine] + doctrines[fed_b][doctrine]) / 2, 2
            )

            doctrines[fed_a][doctrine] = avg_weight
            doctrines[fed_b][doctrine] = avg_weight

            balancing_actions.append(
                {
                    "doctrine": doctrine,
                    "balanced_weight": avg_weight,
                    "federations": [fed_a, fed_b],
                }
            )

        if balancing_actions:

            DOCTRINAL_BALANCE["equilibrium_state"] = "REBALANCED"

        DOCTRINAL_BALANCE["balancing_events"].extend(balancing_actions)

    except Exception as e:

        print("❌ DOCTRINE BALANCING ERROR:")

        print(str(e))

    return balancing_actions


# =========================================================
# 🔥 FETCH BALANCE STATE
# =========================================================


def get_doctrinal_balance_state():

    return DOCTRINAL_BALANCE
